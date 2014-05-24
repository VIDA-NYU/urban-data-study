#ifndef NEIGHBORHOODS_HPP
#define NEIGHBORHOODS_HPP

#include <stdio.h>
#include <vector>
#include <boost/unordered_map.hpp>
#include <cstring>
#include <iostream>

class Neighborhoods
{
public:

  typedef std::vector< std::pair<float,float> > Geometry;
  typedef boost::unordered_map<int, Geometry> GeometryMap;

  Neighborhoods() {}
  
  Neighborhoods(const char *filename)
  {
    this->loadFromFile(filename);
  }
  
  void loadFromFile(const char *filename)
  {
    char name[128];
    int N, nPoly, nPoint;
    float lat, lon;
    Geometry poly;
    
    FILE *fi = fopen(filename, "r");
    fscanf(fi, "%d", &N);
    fgets(name, sizeof(name), fi);
    
    this->geometries.clear();    
    for (int i=0; i<N; i++) {
      fgets(name, sizeof(name), fi);
      name[strlen(name)-1] = 0;
      poly.clear();
      fscanf(fi, "%d\n", &nPoly);
      for (int j=0; j<nPoly; j++) {
        fscanf(fi, "%d\n", &nPoint);
        for (int k=0; k<nPoint; k++) {
          fscanf(fi, "%f %f\n", &lon, &lat);
          poly.push_back(std::make_pair(lat, lon));
        }
      }
      this->geometries[atoi(name)] = poly;
    }
    fclose(fi);
    std::cout<<"File loaded! Number of elements: "<<geometries.size()<<std::endl;
  }

 static void getBounds(const Geometry &geom, float bounds[4])
  {
    if (geom.size()==0) {
      bounds[0] = bounds[1] = -1e30;
      bounds[2] = bounds[3] = 1e30;
    }
    else {
      bounds[0] = bounds[1] = 1e30;
      bounds[2] = bounds[3] = -1e30;
      for (size_t i=0; i<geom.size(); i++) {
        if (geom[i].first<bounds[0]) bounds[0] = geom[i].first;
        if (geom[i].first>bounds[2]) bounds[2] = geom[i].first;
        if (geom[i].second<bounds[1]) bounds[1] = geom[i].second;
        if (geom[i].second>bounds[3]) bounds[3] = geom[i].second;
      }
    }
  }

  static bool isInside(int nvert, float *vert, float testx, float testy)
  {
    if (nvert<=0) return true;
    float firstX = vert[0];
    float firstY = vert[1];
    int i, j, c = 0;
    for (i = 1, j = 0; i < nvert; j = i++) {
      if ( ((vert[i*2+1]>testy) != (vert[j*2+1]>testy)) &&
           (testx < (vert[j*2]-vert[i*2]) * (testy-vert[i*2+1]) / (vert[j*2+1]-vert[i*2+1]) + vert[i*2]) )
        c = !c;
      if (vert[i*2]==firstX && vert[i*2+1]==firstY) {
        if (++i<nvert) {
          firstX = vert[i*2];
          firstY = vert[i*2+1];
        }
      }
    }
    return c;
  }

  bool isInsidePoly(int zipcode, float lat, float lon)
  {
    Geometry vert = geometries[zipcode];
    int nvert = vert.size();
    int i, j, c = 0;
    for (i = 0, j = nvert-1; i < nvert; j = i++) {
      if ( ((vert[i].second>lon) != (vert[j].second>lon)) &&
         (lat < (vert[j].first-vert[i].first) * (lon-vert[i].second) / (vert[j].second-vert[i].second) + vert[i].first) )
         c = !c;
    }
    return c;
  }

private:
  GeometryMap geometries;
};

#endif
