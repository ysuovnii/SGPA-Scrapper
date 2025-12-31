#include <bits/stdc++.h>
#include <curl/curl.h>
#include <gumbo.h>
using namespace std;


size_t writeCallback(void* contents, size_t size, size_t nmemb, string* s) {
    size_t totalSize = size * nmemb;
    s->append((char*)contents, totalSize);
    return totalSize;
}

string httpGet(const string& url) {
    CURL* curl = curl_easy_init();
    string response;

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return response;
}

string findValueByLabel(GumboNode* node, const string& label) {
    if (node->type != GUMBO_NODE_ELEMENT) return "";

    GumboElement* el = &node->v.element;

    if (el->tag == GUMBO_TAG_TD && el->children.length == 1) {
        GumboNode* textNode = (GumboNode*)el->children.data[0];
        if (textNode->type == GUMBO_NODE_TEXT &&
            label == textNode->v.text.text) {

            GumboNode* parent = node->parent;
            GumboVector* siblings = &parent->v.element.children;

            for (size_t i = 0; i + 1 < siblings->length; i++) {
                if (siblings->data[i] == node) {
                    GumboNode* next = (GumboNode*)siblings->data[i + 1];
                    if (next->type == GUMBO_NODE_ELEMENT &&
                        next->v.element.children.length == 1) {
                        GumboNode* valueNode =
                            (GumboNode*)next->v.element.children.data[0];
                        if (valueNode->type == GUMBO_NODE_TEXT)
                            return valueNode->v.text.text;
                    }
                }
            }
        }
    }

    for (size_t i = 0; i < el->children.length; i++) {
        string res = findValueByLabel(
            (GumboNode*)el->children.data[i], label);
        if (!res.empty()) return res;
    }
    return "";
}


struct Student {
    string rollName;
    double sgpa;
    int rank;
};

int main() {
    vector<char> branchList = {'b', 'c', 'e', 'i', 'm', 't', 'v'};
    int sem = 2;

    string filename = "Sem_" + to_string(sem) + "_Result.txt";
    vector<Student> students;

    vector<pair<int, int>> rollRanges = {
        {sem * 1000 + 1, sem * 1000 + 99},
        {sem * 1000 + 101, sem * 1000 + 199}
    };

    for (char branch : branchList) {
        for (auto [start, end] : rollRanges) {
            for (int roll = start; roll < end; roll++) {
                string url =
                    "http://results.ietdavv.edu.in/DisplayStudentResult?rollno=24" +
                    string(1, branch) + to_string(roll) +
                    "&typeOfStudent=Regular";

                string html = httpGet(url);
                GumboOutput* output = gumbo_parse(html.c_str());

                string name = findValueByLabel(output->root, "Student Name");
                string sgpaStr = findValueByLabel(output->root, "SGPA");
                string rollNumber = findValueByLabel(output->root, "Roll Number");

                if (!name.empty() && !sgpaStr.empty() && !rollNumber.empty()) {
                    double sgpa = stod(sgpaStr);
                    students.push_back({
                        rollNumber + " " + name,
                        sgpa,
                        0
                    });
                    cout << "Saved: " << rollNumber << " " << name
                         << " : " << sgpa << endl;
                } else {
                    cout << "Result not found for roll: 24"
                         << branch << roll << endl;
                }

                gumbo_destroy_output(&kGumboDefaultOptions, output);
            }
        }
    }


    sort(students.begin(), students.end(),
         [](const Student& a, const Student& b) {
             return a.sgpa > b.sgpa;
         });

    int rank = 1;
    double prevSGPA = -1;

    for (int i = 0; i < students.size(); i++) {
        if (i == 0 || students[i].sgpa < prevSGPA)
            rank = i + 1;
        students[i].rank = rank;
        prevSGPA = students[i].sgpa;
    }


    ofstream out(filename);
    for (auto& s : students) {
        out << s.rank << ". " << s.rollName
            << " : " << s.sgpa << "\n";
    }
    out.close();

    cout << "File updated with sorted ranks!" << endl;
    return 0;
}
