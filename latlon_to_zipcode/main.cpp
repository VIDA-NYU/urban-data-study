#include "KdTreeBB.hpp"
#include "Neighborhoods.hpp"
#include <string>
#include <sstream>
#include <fstream>
#include <stdlib.h>
#include <iostream>
#include <cstring>
KdTreeBB::Item* loadItems(char* file, KdTreeBB::Item* &items, int &size)
{
	std::ifstream in(file);
	std::string line;
	
	float left, right, top, bottom;
	int zipcode;

	std::getline(in, line);
	size = atoi(line.c_str()); //number of lines
	items = (KdTreeBB::Item*)malloc(sizeof(KdTreeBB::Item)*size);
	int *zipCodes = (int*)malloc(sizeof(int)*size);
	int index = 0;
	while(std::getline(in, line))
	{
		std::stringstream  lineStream(line);
		sscanf(line.c_str(), "%d %f %f %f %f", &zipcode, &left, &bottom, &right, &top);

		items[index].bbox[0][0] = left;
		items[index].bbox[0][1] = right;
		items[index].bbox[1][0] = bottom;
		items[index].bbox[1][1] = top;
		zipCodes[index] = zipcode;
		items[index].data = zipCodes+index;
		index ++;
	}
	return items;
}

void Initialize(Neighborhoods &nb, KdTreeBB &kdtree)
{
	//Create KDTree
  int size;
  KdTreeBB::Item* items;
  loadItems("converted_shapefile/bbox.csv", items, size);
  kdtree.createKdTree(items, size);

	nb.loadFromFile("converted_shapefile/point.txt");
}

int searchZipCode(float lat, float lon, Neighborhoods &nb, const KdTreeBB &kdtree)
{
	KdTreeBB::Query q;
	q.setViewport(lon, lat, lon, lat);
  KdTreeBB::QueryResult result;
  kdtree.query(q, result);

	for (int i=0; i<result.size();i++)
		if (nb.isInsidePoly(result[i], lat, lon)) return result[1];
	return -1;
}

void convert(const char *filename, Neighborhoods &nb, const KdTreeBB &kdtree)
{
	std::ifstream in(filename);
	std::string line;
	std::set<int> zips;

	float lat, lon;
	while(std::getline(in, line))
	{
		try
		{
			std::cout<<line<<std::endl;
			sscanf(line.c_str(), "%f,%f", &lat, &lon);
			int zip = searchZipCode(lat, lon, nb, kdtree);
			if (zip != -1)
				zips.insert(zip);
		}
		catch (...)
		{
			std::cout<<"Exception: "<<line<<std::endl;
		}
	}

	//Write zip code to file
	std::string output = std::string(filename) + std::string(".zipcode");
	std::ofstream outFile;
	outFile.open(output.c_str());
	for (std::set<int>::iterator it=zips.begin(); it!=zips.end(); ++it)
		if (*it > 0)
			outFile <<*it<<std::endl;
	outFile.close();
}

void convert_all(char *filename, Neighborhoods &nb, const KdTreeBB &kdtree)
{
  std::ifstream in(filename);
  std::string line;

	while(std::getline(in, line))
	{
		std::cout<<line<<std::endl;
		convert(line.c_str(), nb, kdtree);
	}
}

int main(int argc, char** argv)
{
	KdTreeBB kdtree;
	Neighborhoods nb;
	Initialize(nb, kdtree);
	
	//search Kdtree
	if (argc==3)
  {
  	float lat = atof(argv[1]);
	  float lon = atof(argv[2]); 
	  fprintf(stderr, "Zipcode: %d\n", searchZipCode(lat, lon, nb, kdtree));
  }
  else
	  convert_all("latlon.txt", nb, kdtree);
	return 0;
}
