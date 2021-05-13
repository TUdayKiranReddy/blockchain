#include "functions.cpp"
#include <iostream>


int main(){
	std::cout << shamir_trick<int>(10, 10, 10, 10, 10)<<std::endl;

	return 0;
}