# `weodata`

The function of this module is simply to download the IMF World Economic Outlook dataset in `pandas.DataFrame`.

### How to Use
```
import weodata
```
The following will download the dataset in a plain `DataFrame`.
```
weodata.load()
```
There are three options:
* `multi_index=True` (default is `False`) returns a `DataFrame` with `MultiIndex` (`countrycode` and `year` as hierarchical row labels):
  ```
  weodata.load(multi_index=True)
  ```
* `description=True` (default is `False`) shows variable definitions.
  ```
  weodata.load(description=True)
  ```
  Given that some column widths are large, you may want to directly access `./archive_weo/indicators.csv`
* `country=True` (default is `False`) shows the list of full country names along with their abbreviation.
  ```
  weodata.load(country=True)
  ```

If you excute `weodata.load()`, a directory `./archive_weo` is automatically created with two files for your reference:
* `indicators.csv` (description of variables)
* `country.csv` (list of full country names)


### How to Install
```
$ pip install git+https://github.com/spring-haru/weodata.git
```
or
```
git clone https://github.com/spring-haru/weodata.git
pip install .
```
<br>

**Note:**
Part of this module is built on [datasets/imf-weio](https://github.com/datasets/imf-weo).
