//#############################################################################
////
//// Copyright (C) 2014, New York University.
//// All rights reserved.
//// Contact: huy.vo@nyu.edu, kien.pham@nyu.edu
////
//// "Redistribution and use in source and binary forms, with or without 
//// modification, are permitted provided that the following conditions are met:
////
////  - Redistributions of source code must retain the above copyright notice, 
////    this list of conditions and the following disclaimer.
////  - Redistributions in binary form must reproduce the above copyright 
////    notice, this list of conditions and the following disclaimer in the 
////    documentation and/or other materials provided with the distribution.
////  - Neither the name of New York University nor the names of its 
////    contributors may be used to endorse or promote products derived from 
////    this software without specific prior written permission.
////
//// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
//// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
//// THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
//// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
//// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
//// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
//// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
//// OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
//// WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
//// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
//// ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
////
////#############################################################################
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
