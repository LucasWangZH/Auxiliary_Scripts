#include <cv.h>
#include <highgui.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include "pa_file.h"
#include <windows.h>
using namespace std;
using namespace cv;


void splitString(const string& s, vector<string>& v, const string& c){
	string::size_type pos1, pos2;
	pos2 = s.find(c);
	pos1 = 0;
	while (string::npos != pos2)
	{
		v.push_back(s.substr(pos1, pos2 - pos1));

		pos1 = pos2 + c.size();
		pos2 = s.find(c, pos1);
	}
	if (pos1 != s.length())
		v.push_back(s.substr(pos1));
}

// void genertorMask(){
// 	string path = "D:/project/openposelab/最新数据/常州标注导线/常州标注汇总/";
// 	vector<string> vec_filename;
// 	paFindFiles(path.c_str(), vec_filename, "*.txt");
// 	int saveCount = 0;
// 	for (int i = 0; i < vec_filename.size(); i++){
// 		ifstream io;
// 		io.open(vec_filename[i]);
// 		if (!io.is_open())
// 			continue;
// 
// 		string fnd = ".txt";
// 		string dst = ".jpg";
// 		string jpgname = vec_filename[i];
// 		jpgname.replace(jpgname.find(fnd), fnd.length(), dst);
// 		Mat frame = imread(jpgname, 1);
// 		if (frame.empty())
// 			continue;
// 		Mat mask = Mat::zeros(frame.size(), CV_8UC1);
// 
// 		int lineCount = 0;
// 		bool needSave = true;
// 		while (!io.eof()){
// 			string buff;
// 			while (getline(io, buff)){
// 
// 				if (!buff.find("daoxian"))
// 					continue;
// 			if (++lineCount <= 2)
// 				continue;
// 
// 			vector<string> vec_splitStr;
// 			vector<Point>  vec_point;
// 			splitString(buff, vec_splitStr, ",");
// 			if (vec_splitStr.size() < 3)
// 				continue;
// 
// 			vec_splitStr.erase(vec_splitStr.begin(), vec_splitStr.begin() + 2);
// 			for (int i = 0; i < vec_splitStr.size(); i += 3){
// 				Point tmpPoint;
// 				tmpPoint.x = atoi(vec_splitStr[i].c_str());
// 				tmpPoint.y = atoi(vec_splitStr[i + 1].c_str());
// 				string tmpStr;
// 				tmpStr = vec_splitStr[i + 2];
// 				vec_point.push_back(tmpPoint);
// 			}
// 
// 
// 			for (int i = 0; i < vec_point.size(); i++){
// 				if (i != vec_point.size() - 1){
// 					line(mask, vec_point[i], vec_point[i + 1], Scalar(255), 2);
// 				}
// 			}
// 		}
// 			needSave = true;
// 		}
// 		if (needSave){
// 			saveCount++;
// 			imwrite(format("D:/project/openposelab/maskdata/%03d.jpg", saveCount), frame);
// 			imwrite(format("D:/project/openposelab/maskdata/%03d_mask.jpg", saveCount), mask);
// 			printf("SAVETO_%d", saveCount);
// 		}
// 	}
// }

void main(){
	string path = "C:/Users/slkj/Desktop/che/6.25标注/";
	vector<string> vec_filename;
	paFindFilesShort(path.c_str(), vec_filename, "*.txt");
	for (int i = 0; i < vec_filename.size(); i++){
		vector<string> vec_split;
		splitString(vec_filename[i], vec_split, "-");
		if (vec_split.size() != 2)
			continue;
		string filename = vec_split[1];
		filename.erase(filename.end() - 5, filename.end());
		string tmp1 = path + vec_split[0] + "-5.txt";
		string tmp2 = path + vec_split[0] + "-7.txt";
		string tmp3 = path + vec_split[0] + "-8.txt";
		CopyFileA((path + vec_filename[i]).c_str(), tmp1.c_str(), true);
		CopyFileA((path + vec_filename[i]).c_str(), tmp2.c_str(), true);
		CopyFileA((path + vec_filename[i]).c_str(), tmp3.c_str(), true);


		//genertorMask();
	}
}