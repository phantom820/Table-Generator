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

### Benchmarks
An experiment was done in which the resulting dataset was as follows. We employed a machine with the
following specs to run the code:
* OS name : Ubuntu 20.04.3 LTS.
* Processor : Intel® Core™ i7-8750H CPU @ 2.20GHz × 12
* Memory: 15.5 GiB

| First Header  | Latex | Html | Word |
| ------------- | ------------- | -------| --- |
| Image Dimension  | 1700 × 2200 × 3   | 1653 × 2339 × 3 | 1700 × 2200 × 3 |
| Image Count  | 10 000  | 10 000 | 10 000 |
| Table Count  | 25 210  | 25 276 | 21 854 |
| Size  | 11.5 GB   | 14.2 GB | 13.8 GB |
| Time  | 2.35 hrs   | 1.5 hrs GB | 1.15 hrs |
The total run time for generating was 5 hrs and total storage was 40 GB.
