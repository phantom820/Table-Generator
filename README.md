# Table-Generator
Tables provide a concise and systematic way of displaying and arrange data of interests. Although tables are
easily identifiable and interpretable to humans this is not the case for machines. With the amount of digital
data available growing exponentially, the amount of data represented in table format also continues to grow.
Typical examples of everyday data that is represented in tables includes invoices, receipts, medical records
and so on. While human beings can read and interpret tables , doing this manually is a time consuming task
and can be error prone. Automated table detection methods are preffered over manual processing of tables.

The purpose of this project was to produce a synthetic dataset that can be used for developing table detection
and table structure recognition methods for the purpose of extracting tabular data from scanned documents. This dataset features tables 
generated from latex, html and word. The actual contents of the table were not regardes as important only the different structures/styling of tables
were taken into consideration. Follow steps below to generate a dataset 


### Dependencies 

First install all the required components by running the following (I know a Docker Image would be better working on it).

```
./configure.sh # note run as sudo
./setup.sh 
pipenv install # note if using pipenv (recommended)
pip install -r requirements.txt # not if not using pipenv
```
### Output Description
Each data point produces has three things, the actual image,  a mask image and an annotation.
* Raw Image - The actual image (PNG) with tables
* Mask - A binary image (PNG) with tables localized.
* Annotation - A json  file containing more info about the tables , has number of tables , bounding boxes and structures.

### Config Description
This a description of important parameters that are specified in the ```config.json``` file.
* ```sample_size (int)``` - how many data points to be produce.
* ```types (List[int])``` - what sort of tables may appear in the dataset (description of each type can be found in types_map)
* ```parallel (boolean)``` - specifies whether the dataset is to be generated sequentially/parallel
* ```img_path (str)``` - path where output images will be saved.
* ```mask_path (str)``` path where output masks will be saved.
* ``` annotaion_path (str) ``` path where annotations will be saved.

### Running
Run the main script i.e
``` python main.py ```
