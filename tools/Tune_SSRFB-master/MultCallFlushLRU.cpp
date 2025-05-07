#include <iostream>
#include <cstdlib>
#include <omp.h>
#include <core_blas.h>

// Generate random number matrix
void Gen_rand_mat(const int m, const int n, double *A)
{
	srand(20210604);

	#pragma omp parallel for
	for (int i=0; i<m*n; i++)
		A[i] = 1.0 - 2.0*(double)rand() / RAND_MAX;
}

#define MAT_SIZE 16384
#define N_IT 50

int main(const int argc, const char **argv)
{
	if (argc < 3)
	{
		std::cerr << "usage: a.out [min NB size] [max NB size]\n";
		return EXIT_FAILURE;
	}

	const int minNB = atoi(argv[1]);
	const int maxNB = atoi(argv[2]);

	// std::cout << "minNB = " << minNB << ", maxNB = " << maxNB << std::endl;
	// std::cout << "wtics = " << omp_get_wtick() << std::endl;

	int nb;   // Tile size
	int ib;   // Inner block size
	double timer;

	double* A = new double [MAT_SIZE * MAT_SIZE];
	double* T = new double[maxNB * maxNB];
	double* W = new double[maxNB * maxNB];

	// Generate random matirx
	Gen_rand_mat(MAT_SIZE, MAT_SIZE, A);
	Gen_rand_mat(maxNB, maxNB, T);

	for (nb = minNB; nb <= maxNB; nb+=32)
	{
		for (ib = 2; ib <= nb/2; ib++)
		{
			if (nb % ib != 0)
				continue;

			double* A1 = A;
			double* A2 = A + nb*nb;
			double* V  = A + 2*nb*nb;

			timer = omp_get_wtime();
			for (int i=0; i<N_IT; i++)
			{
				core_dtsmqr(PlasmaLeft, PlasmaNoTrans, nb, nb, nb, nb, nb, ib, 
					A1, nb, A2, nb, V, nb, T, ib, W, ib);
			}
			timer = omp_get_wtime() - timer;
			std::cout << nb << ", " << ib << ", " << timer / N_IT << std::endl;
		}
	}

	delete [] A;
	delete [] T;
	delete [] W;

	return EXIT_SUCCESS;
}
