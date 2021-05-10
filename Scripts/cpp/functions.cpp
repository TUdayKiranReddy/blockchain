#include <iostream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>
#include <bits/stdc++.h>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/hex.hpp>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>
#include "hash-library/sha256.h"


using namespace boost::multiprecision;
using namespace boost::algorithm;
using namespace boost::random;




cpp_int power(cpp_int x, cpp_int y, cpp_int p)
{
    cpp_int res = 1; 
    x = x % p;  

    while (y > 0)
    {
        if (y & 1)
            res = (res*x) % p;

        y = y>>1;
        x = (x*x) % p;
    }
    return res;
}

bool rabin_muller(cpp_int num){
    cpp_int s = num-1;
    int t = 0;
    int i;
    cpp_int v, a;
    while(s%2==0){
        s = s >> 1;
        ++t;
    }
    for(int trails=0;trails<5;trails++){
        a = 2 + std::rand() % (num - 2);
        v = power(a, s, num);
        if(v!=1){
           i = 0;
           while(v!=num-1){
               if(i==t-1)
                    return false;
                else{
                    ++i;
                    v = (v*v)%num;
                }
           }
        }
    }
    return true;
}


bool is_prime(cpp_int num){
    if(num < 2)
        return false;
    std::vector<int> lowPrimes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997};

    for(int k:lowPrimes){
        if(k==num)
            return true;
    }

    for(int i: lowPrimes){
        if(num%i==0)
            return false;
    }

    return rabin_muller(num);
}

cpp_int generate_large_prime(int num_of_bits){       // Parameterise num_of_bits
    typedef independent_bits_engine<mt19937, 16, cpp_int> generator_type;
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    generator_type gen(seed);
    while(true){
        cpp_int num = gen();
        if(is_prime(num))
            return num;
    }
}

cpp_int* generate_two_distinct_primes(int num_of_bits){
    cpp_int q, p;
    cpp_int* result = new cpp_int[2];
    p = generate_large_prime(num_of_bits);

    while(true){
        q = generate_large_prime(num_of_bits);
        if(q!=p)
            result[0] = p;
            result[1] = q;
            return result;
    }
}

// template <typename T>
// T* xgcd(T b, T a){
//     T prevx, x, prevy, y, q, r;
//     T* result = new T[3];
//     prevx = 1;
//     x = 0;
//     prevy = 0;
//     y = 1;

//     while(a!=0){
//         q, r = floor(b/a);
//         tie(x, prevx) = make_tuple(prevx - q*x, x);
//         tie(y, prevy) = make_tuple(prevy - q*y, y);
//         b, a = a, r;
//     }
//     result[0] = b;
//     result[1] = prevx;
//     result[2] = prevy;

//     return result;
// }


template <typename T>
T xgcd(T a, T b, T &x, T &y) {
    if(b == 0) {
       x = 1;
       y = 0;
       return a;
    }

    T x1, y1, gcd = xgcd<T>(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return gcd;
}

template <typename T>
T mul_inv(T b, T n){
    T result[3];
    result[0] = xgcd<T>(b, n, result[1], result[2]);
    if(result[0]==1)
        return result[1]%n;
    else
        return 0;
}

template <typename T>
T* bezout_coefficients(T a, T b){
    T* result = new T[2];
    T gcd = xgcd(a, b, result[0], result[1]);
    return result;
}

std::string concat(std::vector<std::string> strArray){
    std::string total = std::accumulate(strArray.begin(), strArray.end(), std::string(""));
    return total;
}

template<typename T>
T calculate_product(std::vector<T> lst){
    T i = 1;
    for(T j: lst)
        i *= j;
    return i;
}

cpp_int to_cpp_int(std::string num){
    cpp_int hex=0;
    int i, r;
    int len = num.length();
    if(num.substr(1,2)=="0x"||num.substr(1,2)=="0X")
        num = num.substr(3,len);
    // for(int j=0;j<len;j++){
            
    //     if(strcmp(str[j], '1'))
    //         i+=(1>>4*j);
    //     else if(str[j].compare("2"))
    //         i+=2*(1>>4*j);        
    //     else if(str[j].compare("3"))
    //         i+=3*(1>>4*j);        
    //     else if(str[j].compare("4"))
    //         i+=4*(1>>4*j);        
    //     else if(str[j].compare("5"))
    //         i+=5*(1>>4*j);        
    //     else if(str[j].compare("6"))
    //         i+=6*(1>>4*j);        
    //     else if(str[j].compare("7"))
    //         i+=7*(1>>4*j);        
    //     else if(str[j].compare("8"))
    //         i+=8*(1>>4*j);        
    //     else if(str[j].compare("9"))
    //         i+=9*(1>>4*j);        
    //     else if(str[j].compare("a")||str[j].compare("A"))
    //         i+=10*(1>>4*j);        
    //     else if(str[j].compare("b")||str[j].compare("B"))
    //         i+=11*(1>>4*j);
    //     else if(str[j].compare("c")||str[j].compare("C"))
    //         i+=12*(1>>4*j);
    //     else if(str[j].compare("d")||str[j].compare("D"))
    //         i+=13*(1>>4*j);
    //     else if(str[j].compare("e")||str[j].compare("E"))
    //         i+=14*(1>>4*j);
    //     else if(str[j].compare("f")||str[j].compare("F"))
    //         i+=15*(1>>4*j);
        
    // }
    // return i;

    for (i = 0; num[i] != '\0'; i++)
    {
        len--;
        if(num[i] >= '0' && num[i] <= '9')
            r = num[i] - 48;
        else if(num[i] >= 'a' && num[i] <= 'f')
                r = num[i] - 87;
             else if(num[i] >= 'A' && num[i] <= 'F')
                    r = num[i] - 55;
        hex += r * (1>>4*len);
    }
    return hex;
}

template<typename T>
cpp_int hash_to_length(T x, int num_of_bits){
    //using boost::convert;

    SHA256 sha256;
    //boost::cnv::cstream ccnv;

    int num_of_blocks = ceil(num_of_bits/256);
    std::string pseudo_random_hex_string;
    std::cout << (pseudo_random_hex_string=="") << std::endl;
    for(int i=0;i<num_of_blocks;i++){
        //pseudo_random_hex_string = pseudo_random_hex_string + sha256(convert<std::string>( x+i, ccnv(std::hex)).value_or(NULL));
        pseudo_random_hex_string.append(sha256(boost::lexical_cast<std::string>(x+i))); 
    }
    int r = num_of_bits%256;
    if(r>0)
        pseudo_random_hex_string = pseudo_random_hex_string[(int)(r/4)];
    std::cout << pseudo_random_hex_string << std::endl;
    // T length = convert<int>(pseudo_random_hex_string, ccnv(std::hex)(std::skipws)).value_or(-1);
    //T value = boost::lexical_cast<T>(pseudo_random_hex_string);
    cpp_int value = to_cpp_int(pseudo_random_hex_string);
    return value;
}

int main(){
    // for(int i=0;i<6;i++)
    //     std::cout << generate_large_prime(10) << std::endl;
    // std::cout << sizeof(long long) << std::endl;
    // cpp_int* result = generate_two_distinct_primes(10);
    // std::cout <<  result[0] << std::endl <<result[1] <<std::endl;
    // int result[3];
    // result[0] = xGCD<int>(99, 78, result[1], result[2]);
    // std::cout << result[0] << ' ' << result[1] << ' ' << result[2] << std::endl;
    // int x = mul_inv(3, 17);
    // std::cout << x << std::endl;
    // int* r = bezout_coefficients<int>(55,15);
    // std::cout << r[0]  << ' ' <<r[1]<< std::endl; 
    // std::vector<std::string> str = {"swaroop","swarupa","Rithanyaa","Srivathsava"};
    // std::cout << concat(str) << std::endl;
    // int r = calculate_product<int>(std::vector<int>{1,2,3,4,5});
    // std::cout << r << std::endl;
    std::cout << hash_to_length<cpp_int>(15, 128) << std::endl;

    /* Passing integer vector Arr to the hex function,
    ** this function expects an iterator to write the
    ** resultant hexadecimal value, so we attached
    ** output stream iterator to directly print the value
    */
    //std::string x = "e629fa6598d732768f7c726b4b621285f9c3b85303900aa912017db7617d8bdb";
    //std::cout << x.length()<< std::endl;
    //cpp_int          i(x);
    //std::cout << i<< std::endl;
    return 0;
      // create a new hashing object

}