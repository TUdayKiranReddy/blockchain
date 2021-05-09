#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>

int main()
{
   using namespace boost::multiprecision;
   using namespace boost::random;

   //
   // Declare our random number generator type, the underlying generator
   // is the Mersenne twister mt19937 engine, and we'll generate 256 bit
   // random values, independent_bits_engine will make multiple calls
   // to the underlying engine until we have the requested number of bits:
   //
   typedef independent_bits_engine<mt19937, 256, cpp_int> generator_type;
   generator_type gen;
   //
   // Generate some values:
   //
   std::cout << std::hex << std::showbase;
   for(unsigned i = 0; i < 10; ++i)
      std::cout << gen() << std::endl;
   //
   // Alternatively if we wish to generate random values in a fixed-precision
   // type, then we must use an unsigned type in order to adhere to the
   // conceptual requirements of the generator:
   //
   typedef independent_bits_engine<mt19937, 512, uint512_t> generator512_type;
   generator512_type gen512;
   //
   // Generate some 1024-bit unsigned values:
   //
   std::cout << std::hex << std::showbase;
   for(unsigned i = 0; i < 10; ++i)
      std::cout << gen512() << std::endl;
      return 0;
}