//#include "functions.h"

#include <iostream>
#include <cstdlib>
#include <vector>
#include <map>
#include <cmath>
#include <string>
#include <algorithm>
#include <bits/stdc++.h>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/hex.hpp>
#include <boost/convert.hpp>
#include <boost/convert/stream.hpp>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>
#include "sha256.h"

using boost::convert;
using namespace boost::multiprecision;
using namespace boost::algorithm;
using namespace boost::random;

 
struct boost::cnv::by_default : public boost::cnv::cstream {};

int RSA_KEY_SIZE  =2048;
int ACCUMULATED_PRIME_SIZE= 128;
int RSA_PRIME_SIZE = 1024;


template<typename T>
T rand_gen(){
    typedef independent_bits_engine<mt19937, 256, T> generator_type;
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    
    generator_type gen(seed);
    return gen();
}

template<typename T>
cpp_int randbelow(T ulim, T llim=0){
    mt19937 mt;
    uniform_int_distribution<cpp_int> ui((cpp_int(llim+1) << 256), cpp_int(ulim-1) << 256);

    return ui(mt);
}

template<typename T>
T power(T x, T y, T p)
{
    T res = 1; 
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
    typedef independent_bits_engine<mt19937, 1024, cpp_int> generator_type1;
    typedef independent_bits_engine<mt19937, 256, cpp_int> generator_type2;
    if(num_of_bits > 256){
        
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        generator_type1 gen1(seed);
        while(true){
            cpp_int num = gen1();
            if(is_prime(num))
                return num;
        }
    }
    else{
        
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        generator_type2 gen2(seed);
        while(true){
            cpp_int num = gen2();
            if(is_prime(num))
                return num;
        }
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


template<typename T>
cpp_int hash_to_length(T x, int num_of_bits){

    boost::cnv::cstream ccnv;
    SHA256 sha256;

    double num_of_blocks = ceil((double)num_of_bits/256);
    std::string pseudo_random_hex_string;
    for(int i=0;i<num_of_blocks;i++){

        pseudo_random_hex_string.append(sha256(boost::lexical_cast<std::string>(x+i))); 
    }
    int r = num_of_bits%256;
    if(r>0)
        pseudo_random_hex_string = pseudo_random_hex_string.substr((int)(r/4), pseudo_random_hex_string.length());


    cpp_int value=convert<cpp_int>(pseudo_random_hex_string, ccnv(std::hex)(std::skipws)).value_or(0);;

    return value;
}

template<typename T>
cpp_int* hash_to_prime(T x, int num_of_bits=128, int nonce=0){
    cpp_int* num = new cpp_int[2];
    while(true){
        num[0] = hash_to_length<T>(x + nonce, num_of_bits);
        if(is_prime(num[0])){
            num[1] = nonce;
            return num;
        }
        nonce++;
    }
}

template<typename T>
T shamir_trick(T pi1, T pi2, T x1, T x2, T n){
    T* bzc = bezout_coefficients<T>(x1, x2);
    T positive_a, positive_b, inverse_pi1, inverse_pi2, power1, power2, pi;
    if(bzc[0] < 0){
        positive_a = -1*bzc[0];
        inverse_pi2 = mul_inv<T>(pi2, n);
        power1 = power<T>(pi1, bzc[1], n);
        power2 = power<T>(inverse_pi2, positive_a, n);
    }
    else if(bzc[1] > 0){
        positive_b = -1*bzc[1];
        inverse_pi1 = mul_inv<T>(pi1, n);
        power1 = power<T>(inverse_pi1, positive_b, n);
        power2 = power<T>(pi2, bzc[0], n);
    }
    else{
        power1 = power<T>(pi1, bzc[1], n);
        power2 = power<T>(pi2, bzc[0], n);
    }
    pi = power1*power2;
    return pi;
}

template<typename T>
T* create_list(int size){
    T *res = new T[size];
    for(int i =0; i<size;i++){
        res[i]=(rand_gen<T>());
    }
    return res;
}

// std::std::map<cpp_int, int> setup(cpp_int* n, cpp_int* A0){
//     cpp_int* primes = generate_two_distinct_primes(RSA_PRIME_SIZE);
//     n = primes[0]*primes[0];

//     A0 = 
// }


int main(){


    //cpp_int* res = create_list<cpp_int>(10);
    cpp_int x;
    cpp_int lim = 100;
    for(int i=0;i<10;i++){
        x = randbelow<cpp_int>(lim);
        std::cout << x << " "  << x<= lim << std::endl;
    }
    return 0;
}