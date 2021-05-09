//#include <boost/multiprecision/cpp_int.hpp>

//using namespace boost::multiprecision;

//int main() {
//boost::uint64_t i = (std::numeric_limits<boost::uint64_t>::max)();
//boost::uint64_t j = 1;

//uint128_t ui128, x;
//uint256_t ui256;
////
//// Start by performing arithmetic on 64-bit integers to yield 128-bit results:
////
//x = add(ui128, i, j);
//std::cout << std::hex << std::showbase << i << std::endl;
//std::cout << std::hex << std::showbase << add(ui128, i, j) << std::endl;
//std::cout << std::hex << std::showbase << multiply(ui128, i, i) << std::endl;
//std::cout << "\n" << x << std::endl;
////
//// The try squaring a 128-bit integer to yield a 256-bit result:
////
//ui128 = (std::numeric_limits<uint128_t>::max)();
//std::cout << std::hex << std::showbase << multiply(ui256, ui128, ui128) << std::endl;
//return 0;
//}


//// independent_bits_engine constructor
//#include <iostream>
//#include <chrono>
//#include <cstdint>
//#include <random>

//int main ()
//{
  //typedef std::independent_bits_engine<std::mt19937,64,std::uint_fast64_t> generator_type;

  //generator_type g1;

  //generator_type g2(g1.base());

  //std::mt19937 temp;
  //generator_type g3(std::move(temp));

  //unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  //generator_type g4(seed);

  //std::seed_seq sseq ({2,16,77});
  //generator_type g5(sseq);

  //std::cout << "g1(): " << g1() << std::endl;
  //std::cout << "g2(): " << g2() << std::endl;
  //std::cout << "g3(): " << g3() << std::endl;
  //std::cout << "g4(): " << g4() << std::endl;
  //std::cout << "g5(): " << g5() << std::endl;

  //return 0;
//}

#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <cmath>
#include <ctime>
#include <chrono>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>

using namespace boost::multiprecision;
using namespace boost::random;
using namespace std;

uint256_t rand_gen(){
	typedef independent_bits_engine<mt19937, 256, uint256_t> generator_type;
  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    //srand(time(0));
    generator_type gen(seed);
    return gen();
}

int main()
{

   uint256_t x = rand_gen();
   
   cout << sizeof(uint256_t)*8  << endl;
   
 //   ofstream keyfile;
 //   privatekeyfile.open("inputfile.csv");
   
 //   for(int i = 0; i < 100; i++)
 //        keyfile << rand_gen() << "\n" ;
 //   privatekeyfile.close();
   
 //  // Read the data file
 //  vector<uint256_t> row;
 //  vector<uint256_t> privatekeys;
 //  uint256_t line, word;
 //  //string line, word, temp;
 //  ifstream fin("inputfile.csv");
 //  //int k = 0;
 //  while(!fin.eof())
	// {
	// 	row.clear();
	// 	fin >> line;
	// 	//stringstream s(line);
	// 	cout << line << "\n";
	// 	keys.push_back(line);
        
	// }
	// cout << "\n" << "The private keys are as follows";
	// for(int i=0; i < 100; i++)
	// 	cout << keys[i] << "\n";
 //   //
 //   // Declare our random number generator type, the underlying generator
 //   // is the Mersenne twister mt19937 engine, and we'll generate 256 bit
 //   // random values, independent_bits_engine will make multiple calls
 //   // to the underlying engine until we have the requested number of bits:
 //   //
 //      //
 //   // Alternatively if we wish to generate random values in a fixed-precision
 //   // type, then we must use an unsigned type in order to adhere to the
 //   // conceptual requirements of the generator:
 //   //
 //   //typedef independent_bits_engine<mt19937, 512, uint512_t> generator512_type;
 //   //generator512_type gen512;
 //   //
 //   // Generate some 1024-bit unsigned values:
 //   //
 //   //std::cout << std::hex << std::showbase;
 //   //for(unsigned i = 0; i < 10; ++i)
 //    //  std::cout << gen512() << std::endl;
 //      return 0;
}
