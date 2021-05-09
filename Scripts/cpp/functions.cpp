#include <iostream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <algorithm>
#include <bits/stdc++.h>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>


using namespace boost::multiprecision;
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

template <typename T>
T* xgcd(T b, T a){
    T x0, x1, y0, y1, q;
    T* result = new T[3];
    x0 = 1;
    x1 = 0;
    y0 = 0;
    y1 = 1;

    while(a!=0){
        q, b, a = b/a, a, b%a;
        x0, x1 = x1, x0 - q * x1;
        y0, y1 = y1, y0 - q * y1;
    }
    result[0] = b;
    result[1] = x0;
    result[2] = y0;

    return result;
} 

int main(){
    // for(int i=0;i<6;i++)
    //     std::cout << generate_large_prime(10) << std::endl;
    // std::cout << sizeof(long long) << std::endl;
    // cpp_int* result = generate_two_distinct_primes(10);
    // std::cout <<  result[0] << std::endl <<result[1] <<std::endl;
    int* r = xgcd<int>(58109, 2579);
    std::cout << r[0] << r[1] << r[2] << std::endl;
    return 0;
}