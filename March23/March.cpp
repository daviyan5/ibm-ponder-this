#include <iostream>
#include <bits/stdc++.h>
#include <stdio.h>
#include <stdlib.h>
#include <gmpxx.h>
#include <chrono>
#include <omp.h>

using namespace std;

// Create a stream to write to a file
ofstream fout("March.txt");
int max_len = 0;
mpz_t ans_int;
auto start = chrono::steady_clock::now();

string get_time(chrono::duration<double> time_passed){
    int hours = time_passed.count() / 3600;
    int minutes = (time_passed.count() - hours * 3600) / 60;
    int seconds = time_passed.count() - hours * 3600 - minutes * 60;
    string time = to_string(hours) + "h:" + to_string(minutes) + "m:" + to_string(seconds) + "s";
    return time;
}
void solve(mpz_t p, int d, int e, int mod3){
    if(e < 0){
        // If p > ans_int, then update ans_int
        #pragma omp critical
        {
        if(mpz_cmp(p, ans_int) > 0){

            string s;
            char *sc = mpz_get_str(NULL, 10, p);
            s = sc;
            auto end = chrono::steady_clock::now();
            
            string time_passed = get_time(end - start);
            fout << "(" << time_passed << ")\t\t" << "Best so far: " << s.size() << " digits"  << "\t\t" << s << endl;

            mpz_set(ans_int, p);
            free(sc);
        }
        }
        return;
    }
    else{
        // new_p = p * 10 + d
        mpz_t new_p;
        mpz_init(new_p); mpz_set(new_p, p);
        mpz_mul_ui(new_p, new_p, 10); mpz_add_ui(new_p, new_p, d);
        #pragma omp parallel for
        for(int d = 0; d <= 9; d++){
            bool wont_check = ((d + mod3) % 3 == 0 or d == 0 or d == 2 or d == 4 or d == 5 or d == 6 or d == 8);
            if(wont_check) solve(new_p, d, e - 1, (mod3 + d) % 3);
            else{
                mpz_t next_p; mpz_init(next_p);
                mpz_set(next_p, new_p);
                mpz_mul_ui(next_p, next_p, 10); mpz_add_ui(next_p, next_p, d);
                int a = mpz_probab_prime_p(next_p, 25);
                if(a) solve(new_p, d, e, (mod3 + d) % 3);
                else solve(new_p, d, e - 1, (mod3 + d) % 3);
                mpz_clear(next_p);
            }
        }
        mpz_clear(new_p);
    }
}
int main(){
    int e = 2;
    mpz_init(ans_int);
    mpz_set_ui(ans_int, 0);
    mpz_t new_p;
    mpz_init(new_p);
    mpz_set_ui(new_p, 0);

    #pragma omp parallel for 
    for(int d = 1; d <= 9; d++){
        bool wont_check = (d == 0 or d == 1 or d == 4 or d == 6 or d == 8 or d == 9);
        if(wont_check) solve(new_p, d, e - 1, d % 3);
        else solve(new_p, d, e, d % 3);
        
    }
    string ans;
    char* ansc = mpz_get_str(NULL, 10, ans_int);
    ans = ansc;
    auto end = chrono::steady_clock::now();
    string time_passed = get_time(end - start);

    fout << "(" << time_passed << ")\t\t" << "Ans = " << ans << endl;

    fout.close();
    free(ansc);
    mpz_clear(ans_int);
    mpz_clear(new_p);
    return 0;
}