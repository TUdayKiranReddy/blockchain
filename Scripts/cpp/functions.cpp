//#include "functions.h"

#include <iostream>
#include <cstdlib>
#include <vector>
#include <map>
#include <list>
#include <cmath>
#include<cstdio>
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
T calculate_product(T* lst, int len){
    T i = 1;
    for(int j=0;j<len;j++)
        i *= lst[j];
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

int T_S = 200;

class HashTableEntry {
   public:
      cpp_int k;
      int v;
      HashTableEntry(cpp_int k, int v) {
         this->k= k;
         this->v = v;
      }
};
class HashMapTable {
   private:
      HashTableEntry **t;
   public:
   		int length=0;
      HashMapTable() {
         t = new HashTableEntry * [T_S];
         for (int i = 0; i< T_S; i++) {
            t[i] = NULL;
         }
      }
      int HashFunc(cpp_int k) {
         return int(k % cpp_int(T_S));
      }
      void Insert(cpp_int k, int v) {
         int h = HashFunc(k);
         std::cout << h << std::endl;
         while (t[h] != NULL && t[h]->k != k) {
            h = HashFunc(h + 1);
         }
         if (t[h] != NULL)
            delete t[h];
         t[h] = new HashTableEntry(k, v);
         length++;
      }
      int SearchKey(cpp_int k) {
         int h = HashFunc(k);
         while (t[h] != NULL && t[h]->k != k) {
            h = HashFunc(h + 1);
         }
         if (t[h] == NULL)
            return -1;
         else
            return t[h]->v;
      }
      void Remove(cpp_int k) {
         int h = HashFunc(k);
         while (t[h] != NULL) {
            if (t[h]->k == k)
               break;
            h = HashFunc(h + 1);
         }
         if (t[h] == NULL) {
            std::cout<<"No Element found at key "<<k<<std::endl;
            return;
         } else {
            delete t[h];
         }
         length--;
         std::cout<<"Element Deleted"<<std::endl;
      }

      cpp_int* keys(){
      	cpp_int* key = new cpp_int[length];
      	int j=0;
      	for(int i=0; i<T_S; i++){
			if(t[i]!=NULL){
				key[j]=t[i]->k;
				j++; 
			}
		}
		return key;
      }

      int* values(){
      	int* value = new int[length];
      	int j=0;
      	for(int i=0; i<T_S; i++){
			if(t[i]!=NULL){
				value[j]=t[i]->v;
				j++; 
			}
		}
		return value;
      }

      void print(){
		std::cout << "{ "; 
		for(int i=0; i<T_S; i++){
			if(t[i]!=NULL)
				std::cout << t[i]->k << ":" << t[i]->v << ", "; 
		}
		std::cout << "\b}" << std::endl;
      }

      ~HashMapTable() {
         for (int i = 0; i < T_S; i++) {
            if (t[i] != NULL)
               delete t[i];
            delete[] t;
         }
      }
};

template<typename T>
T* create_list(int size){
    T *res = new T[size];
    for(int i =0; i<size;i++){
        res[i]=(rand_gen<T>());
    }
    return res;
}



HashMapTable setup(cpp_int &n, cpp_int &A0){
    cpp_int* primes = generate_two_distinct_primes(RSA_PRIME_SIZE);
    n = primes[0]*primes[1];

    A0 = cpp_int(std::rand());
    HashMapTable S;
    return S;
}

cpp_int add(cpp_int A, HashMapTable &S, cpp_int x, cpp_int n){
	if(S.SearchKey(x)!=-1)
		return A;
	else{
		cpp_int* hp_nonce;
		hp_nonce = hash_to_prime(x, ACCUMULATED_PRIME_SIZE);
		A = power(A, hp_nonce[0], n);
		S.Insert(x, int(hp_nonce[1]));
		return A;
	}

}

template<typename T>
T concat_int(T a, T b, T c){
	T Ndigit_b = 1;
	T Ndigit_c = 1;
	while(Ndigit_b<=b)	Ndigit_b*=10;
	while(Ndigit_c<=c)	Ndigit_c*=10;
	return T(Ndigit_b*Ndigit_c)*a + T(Ndigit_c)*b + c;
}

template<typename T>
T* prove_exponentiation(T u, T x, T w, T n){
	T* l_nonce = hash_to_prime(concat_int<T>(x, u, w));
	T q = T(x/l_nonce[0]);
	T* result = new T[2];
	result[0] = power<T>(u, q, n);
	result[1] = l_nonce[1];
	return result;
}

template<typename T>
bool dunder_verify_exponentiation(T Q, int l_nonce, T u, T x , T w, T n){
	T l = hash_to_prime(concat_int<T>(x, u, w), 128, int(l_nonce))[0];
	T r = x % l;
	return ((power(Q, l, n) % n) * (power(u, r, n) % n) % n) == w;
}

template<typename T>
bool verify_exponentiation(T Q, int l_nonce, T u, T x , int x_nonce, T w , T n){
	x = hash_to_prime<T>(x, 128, x_nonce)[0];
	return dunder_verify_exponentiation<T>(Q, l_nonce, u, x, w, n);
}


template<typename T>
T* subarr(T* arr, int len, int start, int end){
	T* subarr = new T[end-start];
	int j = 0;
	for(int i=0; i<len; i++){
		if(i>=start && i < end){
			subarr[j] = arr[i];
			j++;
		}
	}
	return subarr;
}

template<typename T>
T* addarrays(T* a, int a_len, T* b, int b_len){
	int new_len = a_len+b_len;
	T* newarr = new T[new_len];
	for(int i=0;i<new_len;i++){
		if(i<a_len)
			newarr[i] = a[i];
		else
			newarr[i] = b[i-a_len];
	}
	return newarr;
}

template<typename T>
void printArray(T* arr, int len){
	std::cout << "{";
	for(int i=0;i<len;i++)
		std::cout<<arr[i]<<",";
	std::cout << "}" << std::endl;
}

template<typename T>
T* root_factor(T g, T* primes, int primes_len, T N , int &rfactor_len){// , int &l_rfactor_len, int &r_rfactor_len){
	int n = primes_len;
	if(n == 1){
		rfactor_len+=1;
		T* G = new T[1];
		G[0] = g;
		return G;
	}
		
	int n_tag = n / 2;
	std::cout << n_tag << std::endl;
	T* primes_L = subarr<T>(primes, primes_len, 0, n_tag);
	T product_L = calculate_product<T>(primes_L, n_tag);
	// std::cout << "product_L " << product_L << std::endl;
	T g_L = power<T>(g, product_L, N);
	// std::cout << "g_L " << g_L << std::endl;
	
	T* primes_R = subarr<T>(primes, primes_len, n_tag, n);
	T product_R = calculate_product<T>(primes_R, n-n_tag);
	// std::cout << "product_R " << product_R << std::endl;
	T g_R = power<T>(g, product_R, N);
	// std::cout << "g_R " << g_R << std::endl;
	int l_rfactor_len = 0;
	int r_rfactor_len = 0;
	T* L = root_factor<T>(g_R, primes_L, n_tag, N, l_rfactor_len);//, l_rfactor_len, l_rfactor_len);
	T* R = root_factor<T>(g_L, primes_R, n-n_tag, N, r_rfactor_len);//, r_rfactor_len, r_rfactor_len);
	rfactor_len = l_rfactor_len + r_rfactor_len;
	
 	return addarrays<T>(L, l_rfactor_len, R, r_rfactor_len);
 }


cpp_int* batch_add(cpp_int A_pre_add, HashMapTable S, cpp_int* x_list, int x_list_len, cpp_int n){
	cpp_int product = 1;
	cpp_int* result = new cpp_int[3];
	for(int i =0;i<x_list_len;i++){
		if(S.SearchKey(x_list[i])==-1){
			cpp_int* hash_prime_nonce = hash_to_prime<cpp_int>(x_list[i]);
			S.Insert(x_list[i], int(hash_prime_nonce[1]));
			product *= hash_prime_nonce[0];
		}
	}
	cpp_int A_post_add = power<cpp_int>(A_pre_add, product, n);
	cpp_int* pe_result = prove_exponentiation(A_pre_add, product, A_post_add, n);
	result[0] = A_post_add;
	result[1] = pe_result[0];
	result[2] = pe_result[1];
	return result; 
}

cpp_int Delete(cpp_int A0, cpp_int A, HashMapTable S, cpp_int x, cpp_int n){
	if(S.SearchKey(x)==-1){
		return A;
	}
	else{
		S.Remove(x);
		cpp_int product = 1;
		cpp_int* key = S.keys();
		int nonce;
		cpp_int element;
		for(int i=0;i<S.length;i++){
			element = key[i];
			nonce = S.SearchKey(element);
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0];
		}
		cpp_int Anew = power<cpp_int>(A0, product, n);
		return Anew;
	}
}


cpp_int batch_Delete(cpp_int A0, HashMapTable S, cpp_int* x_list, int x_list_len, cpp_int n){
	for(int i=0;i<x_list_len;i++)
		S.Remove(x_list[i]);
		
	if(S.length == 0){
		return A0;
	}
	else{
		cpp_int product = 1;
		cpp_int* key = S.keys();
		int nonce;
		cpp_int element;
		for(int i=0;i<S.length;i++){
			element = key[i];
			nonce = S.SearchKey(element);
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0];
		}
		cpp_int Anew = power<cpp_int>(A0, product, n);
		return Anew;
	}
}

cpp_int prove_membership(cpp_int A0, HashMapTable S, cpp_int x, cpp_int n){
	if (S.SearchKey(x)==-1){
		return -1;
	}
	else{
		cpp_int element, product = 1;
		int nonce;
		cpp_int* key = S.keys();
		for(int i=0;i<S.length;i++){
			element = key[i];
			if(element != x){
				nonce = S.SearchKey(element);
				product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0];
			}
		}
		cpp_int A = power<cpp_int>(A0, product, n);
		return A;
	}
}

cpp_int* prove_membership_with_NIPoE(cpp_int g, HashMapTable S, cpp_int x, cpp_int n, cpp_int w){
	cpp_int* result = new cpp_int[3];
	cpp_int u = prove_membership(g, S, x, n);
	cpp_int* x_prime_nonce = hash_to_prime(x, 128, S.SearchKey(x));
	cpp_int* Q_l_nonce = prove_exponentiation(u, x_prime_nonce[0], w, n);

	result[0] = Q_l_nonce[0];
	result[1] = Q_l_nonce[1];
	result[2] = u;
	return result;
}

template<typename T>
bool finElement(T* arr, int len, T element){
	for(int i=0;i<len;i++){
		if(arr[i]==element){
			return true;
		}
	}
	return false;
}

cpp_int batch_prove_membership(cpp_int A0, HashMapTable S, cpp_int* x_list, int x_list_len, cpp_int n){
	cpp_int product = 1;
	cpp_int* key = S.keys();
	cpp_int element;
	int nonce;
	for(int i =0;i<S.length;i++){
		if(finElement<cpp_int>(x_list, x_list_len, element)){
			nonce = S.SearchKey(element);
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0];
		}
	}
	cpp_int A = power<cpp_int>(A0, product, n);
	return A;
}

cpp_int dunder_calculate_primes_product(cpp_int* x_list, int x_list_len, int* nonce_list, int nonce_list_len){
	if(x_list_len != nonce_list_len)
		return -1;
	
	cpp_int* primes_list = new cpp_int[x_list_len];// [hash_to_prime(x, nonce=nonce_list[i])[0] for i, x in enumerate(x_list)]
	for(int i=0;i<x_list_len;i++)
		primes_list[i] = hash_to_prime(x_list[i], 128, nonce_list[i])[0];
	cpp_int product = calculate_product<cpp_int>(primes_list, x_list_len);
	return product;
}

cpp_int* batch_prove_membership_with_NIPoE(cpp_int A0, HashMapTable S, cpp_int* x_list, int x_list_len, cpp_int n, cpp_int w){
	cpp_int* result = new cpp_int[3];
	cpp_int u = batch_prove_membership(A0, S, x_list, x_list_len, n);
	int* nonce_list = S.values();
	cpp_int product = dunder_calculate_primes_product(x_list, x_list_len, nonce_list, S.length);
	cpp_int* Q_l_nonce = prove_exponentiation(u, product, w, n);
	result[0] = Q_l_nonce[0];
	result[1] = Q_l_nonce[1];
	result[2] = u;
	return result;
}

bool dunder_verify_membership(cpp_int A, cpp_int x, cpp_int proof, cpp_int n){
	return power<cpp_int>(proof, x, n) == A;
}

bool verify_membership(cpp_int A, cpp_int x, int nonce, cpp_int proof, cpp_int n){
	return dunder_verify_membership(A, hash_to_prime(x, ACCUMULATED_PRIME_SIZE, nonce)[0], proof, n);
}

bool batch_verify_membership(cpp_int A,cpp_int* x_list, int x_list_len, int* nonce_list, int nonce_list_len, cpp_int proof, cpp_int n){
	cpp_int product = dunder_calculate_primes_product(x_list, x_list_len, nonce_list, nonce_list_len);
	return dunder_verify_membership(A, product, proof, n);
}

bool batch_verify_membership_with_NIPoE(cpp_int Q, int l_nonce, cpp_int u, cpp_int* x_list, int x_list_len, int* nonce_list, int nonce_list_len, cpp_int w, cpp_int n){
	cpp_int product = dunder_calculate_primes_product(x_list, x_list_len, nonce_list, nonce_list_len);
	return dunder_verify_exponentiation<cpp_int>(Q, l_nonce, u, product, w, n);	
}

template<typename T>
T* create_all_membership_witnesses(T A0, HashMapTable S, T n){
	T* primes = new T[S.length];
	cpp_int* key = S.keys();
	for(int i=0;i<S.length;i++)
		primes[i] = hash_to_prime(key[i], ACCUMULATED_PRIME_SIZE, S.SearchKey(key[i]))[0];
	// printArray(primes)
	int rfactor_len=0;
	return root_factor(A0, primes, S.length, n, rfactor_len);
}

cpp_int* prove_non_membership(cpp_int A0, HashMapTable S, cpp_int x, int x_nonce, cpp_int n){
	if(S.SearchKey(x)!=-1)
		return NULL;
	else{
		cpp_int* result = new cpp_int[2];
		cpp_int product = 1;
		cpp_int* key = S.keys();
		cpp_int element;
		int nonce;
		for(int i=0;i<S.length;i++){
			element = key[i];
			nonce = S.SearchKey(element);
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0];
		}
		cpp_int prime = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, x_nonce)[0];
		cpp_int* a_b = bezout_coefficients<cpp_int>(prime, product);
		if(a_b[0] < 0){
			cpp_int positive_a = -1*a_b[0];
			cpp_int inverse_A0 = mul_inv<cpp_int>(A0, n);
			result[0] = power<cpp_int>(inverse_A0, positive_a, n);
		}
		else{
			result[0] = power<cpp_int>(A0, a_b[0], n);
		}
		result[1] = a_b[1];
		return result;
	}
}
		
bool verify_non_membership(cpp_int A0, cpp_int A_final, cpp_int d, cpp_int b, cpp_int x, int x_nonce, cpp_int n){
	cpp_int prime = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, x_nonce)[0];
	cpp_int second_power;
	if(b < 0){
		cpp_int positive_b = -1*b;
		cpp_int inverse_A_final = mul_inv<cpp_int>(A_final, n);
		second_power = power<cpp_int>(inverse_A_final, positive_b, n);
	}
	else{
		second_power = power<cpp_int>(A_final, b, n);
	}
	return ((power<cpp_int>(d, prime, n) * second_power) % n) == A0;
}
	
cpp_int* aggregate_membership_witnesses(cpp_int A, cpp_int* witnesses_list, cpp_int* x_list, int x_list_len, int* nonce_list, int nonce_list_len, cpp_int n){
	cpp_int* primes = new cpp_int[x_list_len];
	for(int i=0;i<x_list_len;i++)
		primes[i]=hash_to_prime(x_list[i], ACCUMULATED_PRIME_SIZE, nonce_list[i])[0];
	
	// printArray<cpp_int>(primes);	
	cpp_int agg_wit = witnesses_list[0];
	cpp_int product = primes[0];
	// std::cout << agg_wit << std::endl;
	// std::cout << product << std::endl;
	for(int i=1;i<x_list_len;i++){
		agg_wit = shamir_trick<cpp_int>(agg_wit,witnesses_list[i], product, primes[i], n);
		product *= primes[i];
	}
	cpp_int* result = new cpp_int[3];
	cpp_int* pe_result = prove_exponentiation(agg_wit, product, A, n);
	result[0] = agg_wit;
	result[1] = pe_result[0];
	result[2] = pe_result[1];
	return result; 
}

cpp_int* batch_delete_using_membership_proofs(cpp_int A_pre_delete, HashMapTable S, cpp_int* x_list, int x_list_len, cpp_int* proofs_list, int proofs_list_len, cpp_int n, int** agg_indexes, int agg_indexes_len){
	bool is_aggregated = agg_indexes_len > 0;
	if(is_aggregated && (proofs_list_len != agg_indexes_len))
		return NULL;
	if(!is_aggregated && (x_list_len != proofs_list_len))
		return NULL;
		
	cpp_int* members = new cpp_int[x_list_len];
	int members_len = x_list_len;
	cpp_int product;
	if(is_aggregated){
		// sanity - verify each and every proof individually
		members = new cpp_int[agg_indexes_len];
		members_len = agg_indexes_len;
		int* indexes = new int[2];
		for(int i=0;i<agg_indexes_len;i++){
			indexes = agg_indexes[i];
			cpp_int* current_x_list = subarr<cpp_int>(x_list, x_list_len, indexes[0], indexes[1]);
			int current_x_list_len = indexes[1]-indexes[0];
			int* current_nonce_list = new int[current_x_list_len];
			for(int j=0;j<current_x_list_len;j++)
				current_nonce_list[j] = S.SearchKey(current_x_list[j]);

			product = dunder_calculate_primes_product(current_x_list, current_x_list_len,  current_nonce_list, current_x_list_len);
			members[i] = product;
			for(int j=0;j<current_x_list_len;j++)
				S.Remove(current_x_list[j]);
		}
	}
				
	else{
		cpp_int x;
		for(int i=0;i<x_list_len;i++){
			x = x_list[i];
			members[i] = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, S.SearchKey(x))[0];
			S.Remove(x);
		}
	}
			
	cpp_int A_post_delete = proofs_list[0];
	product = members[0];
	
	for(int i=1;i<members_len;i++){
		A_post_delete = shamir_trick<cpp_int>(A_post_delete, proofs_list[i], product, members[i], n);
		product *= members[i];
	}
	cpp_int* result = new cpp_int[4];
	cpp_int* pe_result = prove_exponentiation(A_post_delete, product, A_pre_delete, n);
	result[0] = A_post_delete;
	result[1] = product;
	result[2] = pe_result[0];
	result[3] = pe_result[1];
	return result; 
}

void witness_update_after_batch_delete(cpp_int A_post_delete, cpp_int product, HashMapTable S, HashMapTable proofs, cpp_int n){
	cpp_int* key = S.keys();
	cpp_int x;
	cpp_int hash_prime;
	for(int i=0;i<S.length;i++){
		x = key[i];
		hash_prime = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, S.SearchKey(x))[0];
		proofs.Insert(x, int(shamir_trick<cpp_int>(A_post_delete, cpp_int(proofs.SearchKey(x)), product, x, n)));
	}					
}

int main(){
	int* x = new int[6];
	x[0] = 2;
	x[1] = 3;
	x[2] = 5;
	x[3] = 7;
	x[4] = 11;
	x[5] = 13;
	int* s = subarr(x, 6, 2, 4);
	for(int i=0;i<2;i++);
		// std::cout << s[i] << std::endl;
	int* n = addarrays(x, 6, s, 2);
	printArray<int>(n, 8);
	int len, l_len, r_len;
	len = 0;
	l_len = 0;
	r_len = 0;
	int* y = root_factor<int>(55, x, 6, 51, len);
	std::cout << len << std::endl;
	printArray(y, len); 
	std::cout << finElement<int>(x, 6, 2) << std::endl;
	// HashMapTable hash;
	// cpp_int k = rand_gen<cpp_int>();
	// int v = 59;
	// hash.Insert(k, v);
	// cpp_int k1 = rand_gen<cpp_int>();
	// int v1 = 85541359;
	// cpp_int k2 = rand_gen<cpp_int>();
	// int v2 = 99;
	// hash.Insert(k1, v1);
	// hash.Insert(k2, v2);
	// hash.Remove(k1);
	// std::cout << hash.SearchKey(k1) << std::endl;
	// hash.print();
    // cpp_int* res = create_list<cpp_int>(10);
    // std:cout << res[0] << std::endl;
 //    cpp_int n, A0;
 //    HashMapTable S = setup(n, A0);
 //    cpp_int x  = std::rand();
	// cpp_int A1 = add(A0, S, x, n);
	// S.print();
	// std::cout << A0 << std::endl << A1 << std::endl;

    // cpp_int x;
    // cpp_int lim = 100;
    // for(int i=0;i<10;i++){
    //     x = std::rand();
    //     std::cout << x << " "  << (x<= lim) << std::endl;
    // }
    return 0;
}