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
//using namespace cc;

#define min(a, b)  ((a)<(b)?(a):(b))
#define max(a, b)  ((a)>(b)?(a):(b))
float randr(float mi, float mx){
	float acc = rand() / (float)RAND_MAX;
	return acc * (mx - mi) + mi;
}

int randr(int mi, int mx){
	if (mi > mx) std::swap(mi, mx);
	int r = mx - mi + 1;
	return rand() % r + mi;
}


void adBrightness(Mat& img_src, float min, float max)
{
	float alpha = randr((float)min, (float)max);
	int   beta = randr((int)-8, (int)8);
	img_src.convertTo(img_src, CV_8U, alpha, beta);
}

void cropImage(Mat& frame, float pad_scalar, int type){
	Point center;
	float minval;
	float maxval;
	Mat pad_image;
	if (type == 0){
		pad_image = Mat::zeros((1 + pad_scalar)*frame.rows, (1 + pad_scalar)*frame.cols, CV_8UC3);
		center.x = pad_image.cols*0.5;
		center.y = pad_image.rows*0.5;
		Rect roi = Rect(center.x - frame.cols*0.5, center.y - frame.rows*0.5, frame.cols, frame.rows)&Rect(0, 0, pad_image.cols, pad_image.rows);
		frame.copyTo(pad_image(roi));
		minval = min(1 - pad_scalar * 2, 1 + pad_scalar);
		maxval = max(1 - pad_scalar * 2, 1 + pad_scalar);
	}
	else{
		pad_image = frame.clone();
		center.x = pad_image.cols*0.5;
		center.y = pad_image.rows*0.5;
		minval = min(1 - pad_scalar * 2, 1.0f);
		maxval = max(1 - pad_scalar * 2, 1.0f);
	}

	Rect rcOut;
	rcOut.x = center.x - 0.5*randr((float)minval, (float)maxval)*frame.cols;
	rcOut.y = center.y - 0.5*randr((float)minval, (float)maxval)*frame.rows;
	rcOut.width = center.x + 0.5*randr((float)minval, (float)maxval)*frame.cols - rcOut.x;
	rcOut.height = center.y + 0.5*randr((float)minval, (float)maxval)*frame.rows - rcOut.y;
	frame = pad_image(rcOut&Rect(0, 0, pad_image.cols, pad_image.rows));
}

void addNoise(Mat& image, float min_scalar, float max_scalar){

	int min = int(100 * min_scalar);
	int max = int(100 * max_scalar);

	int type = randr(0, 1);
	int p = randr(min, max);
	for (int i = 0; i < image.rows; i++){
		for (int j = 0; j < image.cols; j++){
			if (randr(0, p) != 0)
				continue;

			if (type == 1){
				if (randr(0, 1) == 1){
					image.at<cv::Vec3b>(i, j)[0] = (uchar)(0);
					image.at<cv::Vec3b>(i, j)[1] = (uchar)(0);
					image.at<cv::Vec3b>(i, j)[2] = (uchar)(0);
				}
				else{
					image.at<cv::Vec3b>(i, j)[0] = (uchar)(255);
					image.at<cv::Vec3b>(i, j)[1] = (uchar)(255);
					image.at<cv::Vec3b>(i, j)[2] = (uchar)(255);
				}
			}
			else{
				image.at<cv::Vec3b>(i, j)[0] = (uchar)(randr(0, 255));
				image.at<cv::Vec3b>(i, j)[1] = (uchar)(randr(0, 255));
				image.at<cv::Vec3b>(i, j)[2] = (uchar)(randr(0, 255));
			}
		}
	}
}

void addCutOut(Mat& image, float min_scalar, float max_scalar, int maxNum){
	Mat dst = image.clone();
	int loop = randr(1, maxNum);
	for (int i = 0; i < loop; i++){
		Rect rcTmp;
		rcTmp.x = randr(0, image.cols);
		rcTmp.y = randr(0, image.rows);
		rcTmp.width = randr(min_scalar*image.cols, max_scalar*image.cols);
		rcTmp.height = randr(min_scalar*image.rows, max_scalar*image.rows);
		rcTmp = rcTmp&Rect(0, 0, image.cols, image.rows);
		image(rcTmp).setTo(0);
	}
}

// 	void addRotateImage(Mat& image){
// 		double angle = randr(0, 360.0);
// 		cv::Point2f center(image.cols / 2, image.rows / 2);
// 		cv::Mat rot = cv::getRotationMatrix2D(center, angle, 1);
// 		cv::Rect bbox = cv::RotatedRect(center, image.size(), angle).boundingRect();
// 
// 		rot.at<double>(0, 2) += bbox.width / 2.0 - center.x;
// 		rot.at<double>(1, 2) += bbox.height / 2.0 - center.y;
// 
// 		cv::Mat dst;
// 		cv::warpAffine(image, image, rot, bbox.size());
// 	}

void addMedianBlur(Mat& image, int filterSize){
	cv::medianBlur(image, image, filterSize);
}

void addGaussianBlur(Mat& image, int filterSize){
	float sigma = randr((float)0.1, (float)1.0);
	cv::GaussianBlur(image, image, Size(filterSize, filterSize), sigma, sigma);

}

void addMotionBlur(Mat& srcImg, int filterSize) {
	int size = filterSize;
	cv::Mat filter = cv::Mat::zeros(size, size, CV_8UC1);
	for (int i = 0; i < size; i++)filter.at<uchar>(i, i) = (uchar)1;
	int len = size / 2;
	for (int r = 0; r < srcImg.rows; r++) {
		for (int c = 0; c < srcImg.cols; c++) {
			//mask
			int red = 0, green = 0, blue = 0;
			for (int i = r - len; i <= r + len; i++) {
				for (int j = c - len; j <= c + len; j++) {
					if (i < 0 || j < 0 || i >= srcImg.rows || j >= srcImg.cols) continue;
					blue += ((int)srcImg.at<cv::Vec3b>(i, j)[0]) * ((int)filter.at<uchar>(i - (r - len), j - (c - len)));
					green += ((int)srcImg.at<cv::Vec3b>(i, j)[1]) * ((int)filter.at<uchar>(i - (r - len), j - (c - len)));
					red += ((int)srcImg.at<cv::Vec3b>(i, j)[2]) * ((int)filter.at<uchar>(i - (r - len), j - (c - len)));
				}
			}
			srcImg.at<cv::Vec3b>(r, c)[0] = (uchar)(blue / size);
			srcImg.at<cv::Vec3b>(r, c)[1] = (uchar)(green / size);
			srcImg.at<cv::Vec3b>(r, c)[2] = (uchar)(red / size);
		}
	}
}

void adBlur(Mat& img_src, int maxKenerl)
{
	int nCount = 0;// randr(0, 1);
	if (nCount == 0){
		int kenerl_size = randr(1, 5);
		if (kenerl_size % 2 == 0)
			kenerl_size++;
		addMotionBlur(img_src, kenerl_size);
	}
	else{
		int kenerl_size = randr(1, maxKenerl);
		if (kenerl_size % 2 == 0)
			kenerl_size++;

		if (randr(0, 1) == 0){
			addMedianBlur(img_src, kenerl_size);
		}
		else{
			addGaussianBlur(img_src, kenerl_size);
		}
	}
}

/*
flipCode < 0水平垂直翻转（先沿X轴翻转，再沿Y轴翻转，等价于旋转180°）,
flipCode == 0垂直翻转（沿X轴翻转），
flipCode > 0水平翻转（沿Y轴翻转）
*/


void dataEnlarge(Mat &im){
	//一半概率做图像flip ,级联往下做
	// 		if (randr(0, 1) == 1){
	// 			if (randr(0, 2) == 1){
	// 				flip(im, im, 0);
	// 			}
	// 			if (randr(0, 2) == 1){
	// 				flip(im, im, 1);
	// 			}
	// 			if (randr(0, 2) == 1){
	// 				flip(im, im, -1);
	// 			}
	// // 			if (randr(0, 1) == 1){
	// // 				im = im.t();
	// // 			}
	// 		}

	//对图像进行运动模糊,中值模糊,高斯模糊等操作
	if (randr(0, 1) == 0){
		adBlur(im, 5);
	}

	//对图像进行cutout操作
	/*if (randr(0, 1) == 0){
	addCutOut(im, 0.1, 0.4, 2);
	}*/

	//对图像进行亮度调整
	adBrightness(im, 0.9, 1.1);

	//对图像添加椒盐或者随机噪点
	/*if (randr(0, 2) == 0){
	addNoise(im, 0.1, 0.5);
	}*/

	//对图像进行旋转
	// 		bool brotate = false;
	// 		if (randr(0, 1) == 0){
	// 			addRotateImage(im);
	// 			brotate = true;
	// 		}

	//对图像做crop
	//  		int ntype = 0;
	// 		if (brotate == true){
	// 			ntype = 1;
	// 		}
	if (randr(0, 1) == 0){
		cropImage(im, 0.2, 1);
	 
}

// 	bool mixFrame(Mat& frameIn, const Mat& framemix, float min_scalar, float max_scalar){
// 		if (min(frameIn.cols, frameIn.rows) <= 10 || framemix.empty()){
// 			return false;
// 		}
// 
// 		float alpha = randr(min_scalar, max_scalar);
// 		float beta = (1.0 - alpha);
// 		Mat mixTmp = framemix.clone();
// 		if (mixTmp.size() != frameIn.size()){
// 			resize(mixTmp, mixTmp, frameIn.size());
// 		}
// 		addWeighted(frameIn, beta, mixTmp, alpha, 0.0, frameIn);
// 		return true;
// 	}


int main(){
	string floder = "C:/Users/slkj/Desktop/che/0802最新样本/sideend/";
	PaVfiles vfs;
	//string blur = "blur";
	string gaussblur = "_gaussblur";
	string motionblur = "_motionblur";
	string medianblur = "_medianblur";
	string brightness = "_brightness";
	string noise = "_noise";
	paFindFiles(floder.c_str(), vfs, "*.jpg", false);
	for (auto it : vfs){
		
			Mat im = imread(it.c_str());
			string tmp_file = it;
			tmp_file.erase(tmp_file.begin(), tmp_file.begin() + floder.length());
			tmp_file.erase(tmp_file.end() - 4, tmp_file.end());
			if (randr(0, 5) == 0){
				Mat tmp;
				im.copyTo(tmp);
				addNoise(tmp, 0.1, 0.5);
				imwrite(floder.c_str() + tmp_file + noise + ".jpg", tmp);
			}
			if (randr(0, 5) == 0){
				Mat tmp;
				im.copyTo(tmp);
				int kenerl_size = randr(1, 5);
				if (kenerl_size % 2 == 0)
					kenerl_size++;
				addGaussianBlur(tmp, kenerl_size);
				imwrite(floder.c_str() + tmp_file + gaussblur + ".jpg", tmp);
			}
			if (randr(0, 5) == 0){
				Mat tmp;
				im.copyTo(tmp);
				int kenerl_size = randr(1, 5);
				if (kenerl_size % 2 == 0)
					kenerl_size++;
				addMedianBlur(tmp, kenerl_size);
				imwrite(floder.c_str() + tmp_file + medianblur + ".jpg", tmp);
			}
			if (randr(0, 3) == 0){
				Mat tmp;
				im.copyTo(tmp);
				int kenerl_size = randr(1, 5);
				if (kenerl_size % 2 == 0)
					kenerl_size++;
				addMotionBlur(tmp, kenerl_size);
				imwrite(floder.c_str() + tmp_file + motionblur + ".jpg", tmp);
			}
			//if (randr(0, 5) == 0){
			//	Mat tmp;
			//	im.copyTo(tmp);
			//	adBrightness(tmp, 0.9, 1.1);
			//	imwrite(floder.c_str() + tmp_file + brightness + ".jpg", tmp);
			//}
		
	}
	paFindFiles(floder.c_str(), vfs, "*.txt", false);
	for (auto it : vfs){
		string tmp_file = it;
		tmp_file.erase(tmp_file.begin(), tmp_file.begin() + floder.length());
		tmp_file.erase(tmp_file.end() - 4, tmp_file.end());
		for (int i = 0; i <= 4; i++){
			string tmp;
			if (i == 0){
				tmp = gaussblur;
			}
			else if (i == 1){
				tmp = noise;
			}
			else if (i == 2){
				tmp = medianblur;
			}
			else if (i == 3){
				tmp = motionblur;
			}
			else{
				tmp = brightness;
			}
			CopyFileA(it.c_str(), (floder + tmp_file + tmp + ".txt").c_str(), true);

		}
	}

}