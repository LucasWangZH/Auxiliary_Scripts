#include <Windows.h>
#include <cv.h>
// #include "cc_nb.h"
#include <iostream>
#include <pa_file\pa_file.h>
#include <highgui.h>
#include <fstream>
#include <mutex>
#include <thread>

using namespace cv;
using namespace std;
int main(){
	string video_path = "./test";
	PaVfiles vfs;
	paFindFiles(video_path.c_str(), vfs, "*.avi", false);
	int SAVEGAP = 15;
	for (auto it : vfs){
		VideoCapture capture(it);
		int saveCount = 0;
		Mat frame;
		if (!capture.isOpened()){
			printf("cannot open video \n");
			return -1;
		}
		int frameCount = 0;

		char buff[256];
		paFileName(it.c_str(), NULL, buff);
		string tmp_file = it;
		tmp_file.erase(tmp_file.begin(), tmp_file.begin() + video_path.length());
		tmp_file.erase(tmp_file.end() - 4, tmp_file.end());
		// 		if (it == "s32" || it == "s33" || it == "s34" || it == "s35" || it == "s36")
		// 			SAVEGAP = 15;
		while (capture.read(frame)){
			if (frame.empty())
				return -1;
			if (frameCount++ % SAVEGAP != 0)
				continue;

			imshow("frameShow", frame);
			waitKey(1);

			string tmp_file = it;
			tmp_file.erase(tmp_file.begin(), tmp_file.begin() + video_path.length());
			tmp_file.erase(tmp_file.end() - 4, tmp_file.end());
			imwrite(format("test_jpg/%s_%04d.jpg", buff, saveCount++), frame);
		}


	}

}