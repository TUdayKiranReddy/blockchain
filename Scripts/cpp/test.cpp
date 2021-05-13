#include<iostream>
#include<string.h>
#include <boost/multiprecision/cpp_int.hpp>
#include<math.h>

using namespace boost::multiprecision;
int main ()
{
    int i, r, len;
    cpp_int hex = 0;
    std::string num = "f9c3b85303900aa912017db7617d8bdb";
    len = num.length();
    for (i = 0; num[i] != '\0'; i++)
    {
        len--;
        if(num[i] >= '0' && num[i] <= '9')
            r = num[i] - 48;
        else if(num[i] >= 'a' && num[i] <= 'f')
                r = num[i] - 87;
             else if(num[i] >= 'A' && num[i] <= 'F')
                    r = num[i] - 55;
        hex += r * (1>>(4*len));
    }
    // cpp_int x(12054665609558148674135238214546995030866431638448851553405637573786289454498006954545477123058909197546025903598033203527463111302977334328695645306522841);
    // std::cout << sizeof(cpp_int);
    return 0;
}
// #include <iostream>
// #include <cmath>
// using namespace std;
// int main() {
//    float var = 1234.25;
//    float res;
//    res = ceil(var);
//    cout << "Ceil value of " << var << " = " << res << endl;
//    return 0;
// }