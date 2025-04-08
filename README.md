# 超级图像 Super Image

** 注意：程序为单线程，每次操作未完成时，界面会卡住没有响应，此时不需要点击，只需等待 **  
** Note: The program is single-threaded. When an operation is not completed, the interface will freeze and become unresponsive. Do not click; just wait. **

** 注意：有时候需要点2下才能点击成功 **  
** Note: Sometimes you need to click twice for the action to succeed. **

## 使用步骤 Steps to Use

### 获取微信文章 Fetching WeChat Articles

将微信的PPT图片合订成为PDF文件。  
Combine WeChat PPT images into a PDF file.

- 选择“获取微信文章”  
- Select "Fetch WeChat Articles"

- 输入微信文章URL  
- Enter the WeChat article URL

- 等待下载自动化工具（可能需要一段时间）  
- Wait for the download automation tool (this may take some time)

- 自动化工具下载完成后，会自动打开微信网页，自动将滚动条拉到最下方，然后逐步下载图片、合成PDF  
- Once the automation tool finishes downloading, it will automatically open the WeChat webpage, scroll to the bottom, and gradually download images and combine them into a PDF.

- 等待程序自动操作完毕  
- Wait for the program to complete the automated operation.

### 图片透视变换 Image Perspective Transformation

将手机拍摄的PPT转换成矩形图像，然后可以选择自动合成PDF  
Convert PPTs taken by phone into rectangular images, and optionally combine them into a PDF.

- 将手机照片放在同一个文件夹内（下文称“目标文件夹”）  
- Place the phone photos in the same folder (referred to as the "target folder" below).

** 注意路径中不能有中文 **  
** Note: The path must not contain Chinese characters. **

- 点击左上角“选择目录”，选择目标文件夹  
- Click "Select Directory" in the top left corner to choose the target folder.

- 点击“照片透视变换”  
- Click "Photo Perspective Transformation."

- 每个照片会依次显示在界面上，需要手动点击照片中屏幕的四个角（左上、左下、右下、右上，不限点击顺序）  
- Each photo will be displayed on the interface in sequence. You need to manually click the four corners of the screen in the photo (top left, bottom left, bottom right, top right, in any order).

- 点击完成后会显示变换完成的照片，按ESC键开始下一张照片  
- After clicking, the transformed photo will be displayed. Press the ESC key to start the next photo.

- 转换完成的照片会存储在目标文件夹同级目录下，文件夹名称为目标文件夹名称_result  
- The transformed photos will be stored in a folder at the same level as the target folder, with the folder name being target folder name_result.

### 人工智能识别 AI Recognition

自动识别照片中的显示器，并截取出来。  
Automatically recognize the monitor in the photo and crop it out.

** 注意：受YOLO12限制，此功能不会将显示器变为矩形，会保留显示器原始拍摄角度。 **  
** Note: Due to YOLO12 limitations, this feature will not transform the monitor into a rectangle but will retain the original shooting angle of the monitor. **

- 将手机照片放在同一个文件夹内（下文称“目标文件夹”）  
- Place the phone photos in the same folder (referred to as the "target folder" below).

** 注意路径中不能有中文 **  
** Note: The path must not contain Chinese characters. **

- 点击左上角“选择目录”，选择目标文件夹  
- Click "Select Directory" in the top left corner to choose the target folder.

- 点击“人工智能识别”  
- Click "AI Recognition."

- 识别完成的照片会存储在目标文件夹同级目录下，文件夹名称为目标文件夹名称_result  
- The recognized photos will be stored in a folder at the same level as the target folder, with the folder name being target folder name_result.

### 图像转PDF Image to PDF

将图像和成为PDF文件，会将图片变为1600x900尺寸。  
Convert images into a PDF file, resizing them to 1600x900 dimensions.

- 任意执行完“图片透视变换”或“人工智能识别”之后，点击“图像转PDF”  
- After completing either "Image Perspective Transformation" or "AI Recognition," click "Image to PDF."

- 等待程序执行完毕即可  
- Wait for the program to complete the operation.

## 其他说明 Additional Notes

### 人工智能识 AI Recognition

人工智能识别基于YOLOv12  
AI recognition is based on YOLOv12.

## 源代码打包命令 Source Code Packaging Command

pyinstaller -D -w -i icon.ico --add-data "README.md;." main.py -n SUPER_IMAGE

or

pyinstaller -D -w -i icon.ico --add-data "README.md;." main2.py -n SUPER_IMAGE