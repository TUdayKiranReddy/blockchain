#include "functions.h"
#include <ctime>
#include <chrono>


int main(){
	int N = 10000;
	int K = 4;
	float p = 8.0/(N-1);
	int mean_edges = N*p;
	int X = N*(mean_edges-1)+1;
	int h = int(log(X)/log(mean_edges));
	float T_p = 0.03;
	int R = int(10e6);

	cpp_int n, A0;
	std::chrono::time_point<std::chrono::system_clock> tik, tok;

	HashMapTable S = setup(n, A0);
	int x_len = 100;
	cpp_int* x = create_list<cpp_int>(x_len);

	tik = std::chrono::system_clock::now();
	cpp_int* batch_add_result = batch_add(A0, S, x, x_len, n);
	int W_len = 0;
	
	cpp_int* W = create_all_membership_witnesses(A0, S, n, W_len);
	tok = std::chrono::system_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::microseconds>(tok - tik);
	std::cout << duration.count()*1e-6<< std::endl;

} 