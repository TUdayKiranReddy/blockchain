#include <iostream>
#include <cstdlib>

using namespace std;

struct int64{
	long long value[4];
};

int64 randomNumberGenerator(){
	int64 num;
	srand(time(NULL));
	for(int i=0;i<3;i++){
		num.value[i] = rand();
	}
	return num;
}

int main(){
	int64 hash=randomNumberGenerator();
	cout << hash.value << endl;
	cout << sizeof(hash)*8 << endl;

	
}

