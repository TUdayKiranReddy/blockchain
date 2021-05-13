#define FUNCTIONS_H

#include <iostream>
#include <cstdlib>
#include <vector>
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
#include "hash-library/sha256.h"

using boost::convert;
using namespace boost::multiprecision;
using namespace boost::algorithm;
using namespace boost::random;

 
struct boost::cnv::by_default : public boost::cnv::cstream {};


template<typename T>
T power(T x, T y, T p);

bool rabin_muller(cpp_int num);

bool is_prime(cpp_int num);

cpp_int generate_large_prime(int num_of_bits);

cpp_int* generate_two_distinct_primes(int num_of_bits);

template <typename T>
T xgcd(T a, T b, T &x, T &y);

template <typename T>
T mul_inv(T b, T n);

template <typename T>
T* bezout_coefficients(T a, T b);

std::string concat(std::vector<std::string> strArray);

template<typename T>
T calculate_product(std::vector<T> lst);

template<typename T>
cpp_int hash_to_length(T x, int num_of_bits);

template<typename T>
cpp_int* hash_to_prime(T x, int num_of_bits=128, int nonce=0);

template<typename T>
T shamir_trick(T pi1, T pi2, T x1, T x2, T n);
