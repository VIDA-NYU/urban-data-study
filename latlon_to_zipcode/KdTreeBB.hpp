//#############################################################################
//
// Copyright (C) 2014, New York University.
// All rights reserved.
// Contact: huy.vo@nyu.edu, kien.pham@nyu.edu
//
// "Redistribution and use in source and binary forms, with or without 
// modification, are permitted provided that the following conditions are met:
//
//  - Redistributions of source code must retain the above copyright notice, 
//    this list of conditions and the following disclaimer.
//  - Redistributions in binary form must reproduce the above copyright 
//    notice, this list of conditions and the following disclaimer in the 
//    documentation and/or other materials provided with the distribution.
//  - Neither the name of New York University nor the names of its 
//    contributors may be used to endorse or promote products derived from 
//    this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
// THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
// OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
// WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
// ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
//
//#############################################################################


#ifndef KD_TREE_BB_HPP
#define KD_TREE_BB_HPP

#include <stdint.h>
#include <time.h>
#include <limits.h>
#include <float.h>
#include <vector>
#include <iostream>
#include <cstdio>
#include <algorithm>

class KdTreeBB
{
public:
#pragma pack(push, 1)
  struct Item {
    float    bbox[2][2];
    void    *data;
  };
  
  struct KdNode {
    uint32_t child_node;
    float    leftBounds[2];
    float    rightBounds[2];
  };
#pragma pack(pop)

  static bool dimIntersect(const float a[2], const float b[2]) {
    return std::max(a[0], b[0])<=std::min(a[1], b[1]);
  }
  
  struct Query
  {
    Query() {
      for (int i=0; i<2; i++) {
        this->bounds[i][0] = -FLT_MAX;
        this->bounds[i][1] = FLT_MAX;
      }
    }

    void setViewport(float left, float bottom, float right, float top)
    {
      this->bounds[0][0] = left;
      this->bounds[0][1] = right;
      this->bounds[1][0] = top;
      this->bounds[1][1] = bottom;
    }

    bool isMatched(const Item *item) const
    {
      for (int i=0; i<2; i++)
        if (!dimIntersect(item->bbox[i], this->bounds[i]))
          return false;
      return true;
    }

    float bounds[2][2];
  };
  
  typedef std::vector<int> QueryResult;

public:

  KdTreeBB()
  {
  }

  void query(const Query &q, QueryResult &result) const {
    searchKdTree(this->nodes.data(), 0, 0, q, result);
  }

  void createKdTree(Item *items, int n) {
    this->maxDepth = 0;
    this->nodes.resize(std::max(n*4,1));
    float *tmp = (float*)malloc(sizeof(float)*n);
    int freeNode = 1;
    buildKdTree(this->nodes.data(), tmp, items, n, 0, 0, freeNode);
    fprintf(stderr, "Created a Kd tree for bounding boxes with %d nodes and depth %d.\n", freeNode, this->maxDepth);
    free(tmp);
  }
  
private:
  std::vector<KdNode> nodes;
  int maxDepth;

  void buildKdTree(KdNode *nodes, float *tmp, Item *items, int n, int depth, int thisNode, int &freeNode) {
    KdNode *node = nodes + thisNode;
    int keyIndex = depth%2;
    if (n==0) {
      node->child_node = -1;
      return;
    }
    if (n<2) {
      node->child_node = 0;
      node->leftBounds[0] = items->bbox[keyIndex][0];
      node->leftBounds[1] = items->bbox[keyIndex][1];
      *((void**)(node->rightBounds)) = items->data;
      if (this->maxDepth<depth)
        this->maxDepth = depth;
      return;
    }
    int medianIndex = n/2-1;
    for (size_t i=0; i<n; i++)
      tmp[i] = items[i].bbox[keyIndex][0];
    std::sort(tmp, tmp+n);
    float median = tmp[n/2-1];
    int l = 0;
    int r = n-1;
    while (l<r) {
      while (l<n && items[l].bbox[keyIndex][0]<=median) l++;
      while (r>=0 && items[r].bbox[keyIndex][0]>median) r--;
      if (l<r)
        std::swap(items[l], items[r]);
    }
    medianIndex = r;
    if (medianIndex==n-1)
      medianIndex = n-2;
    node->leftBounds[0] = node->rightBounds[0] = FLT_MAX;
    node->leftBounds[1] = node->rightBounds[1] = -FLT_MAX;
    
    for (unsigned i=0; i<=medianIndex; i++) {
      if (items[i].bbox[keyIndex][0]<node->leftBounds[0])
        node->leftBounds[0] = items[i].bbox[keyIndex][0];
      if (items[i].bbox[keyIndex][1]>node->leftBounds[1])
        node->leftBounds[1] = items[i].bbox[keyIndex][1];
    }
    
    for (unsigned i=medianIndex+1; i<n; i++) {
      if (items[i].bbox[keyIndex][0]<node->rightBounds[0])
        node->rightBounds[0] = items[i].bbox[keyIndex][0];
      if (items[i].bbox[keyIndex][1]>node->rightBounds[1])
        node->rightBounds[1] = items[i].bbox[keyIndex][1];
    }
    
    node->child_node = freeNode;
    freeNode += 2;
    buildKdTree(nodes, tmp, items, medianIndex+1, depth+1, node->child_node, freeNode);
    if (medianIndex<n-1)
      buildKdTree(nodes, tmp, items + medianIndex+1, n-medianIndex-1, depth+1,
                  node->child_node+1, freeNode);
    else
      nodes[node->child_node+1].child_node = -1;
  }

  void searchKdTree(const KdNode *nodes, uint32_t root, int depth, const Query &query, QueryResult &result) const {
    const KdNode *node = nodes + root;
    int rangeIndex = depth%2;

    if (node->child_node==-1) {
	return;
    }
    if (node->child_node==0) {
      if (dimIntersect(node->leftBounds, query.bounds[rangeIndex]))
	{
	//fprintf(stderr, "%d\n", *(*(int**)(node->rightBounds)));
	result.push_back(*(*(int**)(node->rightBounds))); 
	}
        //report(*((void**)(node->rightBounds)));
      return;
    }
    if (dimIntersect(node->leftBounds, query.bounds[rangeIndex]))
      searchKdTree(nodes, node->child_node, depth+1, query, result);
    if (dimIntersect(node->rightBounds, query.bounds[rangeIndex]))
      searchKdTree(nodes, node->child_node+1, depth+1, query, result);
  }    
};

#endif
