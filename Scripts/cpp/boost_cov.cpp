#include <boost/convert.hpp>
#include <boost/convert/stream.hpp>
#include <boost/detail/lightweight_test.hpp>

using std::string;
using boost::convert;

struct boost::cnv::by_default : public boost::cnv::cstream {};


int main(){
	int    i2 = convert<int>("123").value();      // Throws when fails.
	int    i3 = convert<int>("uhm").value_or(-1); // Returns -1 when fails.
	string s2 = convert<string>(123).value();

	std::cout << i2<<std::endl;
	return 0;
}