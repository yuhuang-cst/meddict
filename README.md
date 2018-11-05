# meddict
以现有的中文医学词表以及基于机器翻译的UMLS为基础，**基于规则**进行处理后生成用于分词的**中文**医学词典。

# 文件说明
## 来自人工翻译的词表
`result/segment/thesaurus`文件夹下：

- `hpo.txt`：来自[HPO（官方）](http://www.chinahpo.org/)
- `icd10_gov.txt`：来自[ICD10（官方）](http://www.moh.gov.cn/mohbgt/s6694/201202/54033.shtml)
- `mesh.txt`：来自自[MeSH（非官方）](http://chisc.net/doc/view/9270.html)
- `snomed.txt`：来自[SNOMED（官方）](http://mall.cnki.net/reference/detail_R200908044.html)
- `snomedct.txt`：来自[SNOMED（非官方）](http://chisc.net/doc/view/5201.html)

## 来自UMLS翻译（主要为机器翻译）的词表
`result/segment/umls`文件夹下（根据质量从高到低进行排序）：

- `umls_iciba.txt`：来自金山词霸的带`[医]`字标签的翻译
- `umls_bgequal_baike.txt`：来自百度翻译与谷歌翻译**无序相等且包含中文**的词条，且被[百度百科](https://baike.baidu.com/)或[维基百科](https://zh.wikipedia.org/)所收录
- `umls_bgequal.txt`：来自百度翻译与谷歌翻译**无序相等且包含中文**的词条
- `umls_baike.txt`：来自UMLS的翻译词条，且被[百度百科](https://baike.baidu.com/)或[维基百科](https://zh.wikipedia.org/)所收录
- `umls.txt`：来自UMLS的翻译词条，有待进一步挖掘

## 整合词表
`result/segment/all`文件夹下：

- `meddict_human.txt`：整合上述所有来自人工翻译的词表
- `meddict_human_machine.txt`：整合以下词表
	- 上述所有来自人工翻译的词表
	- `umls_iciba.txt`
	- `umls_bgequal.txt`
	- `umls_baike.txt`

# 词条数目统计
| 词表 | 词条数 |
| ---- | ---- |
| hpo.txt | 11216 |
| icd10_gov.txt | 29080 |
| mesh.txt | 20638 |
| snomed.txt | 10519 |
| snomedct.txt | 116086 |
| umls_iciba.txt | 112755 |
| umls_bgequal_baike.txt | 43763 |
| umls_bgequal.txt | 269181 |
| umls_baike.txt | 163680 |
| umls.txt | 3560886 |
| meddict_human.txt | 166613 |
| meddict_human_machine.txt | 554867 |

# 词表来源
## 现有中文医学词表
- [ICD10（官方）](http://www.moh.gov.cn/mohbgt/s6694/201202/54033.shtml)
- [ICD10（台版）](https://www.nhi.gov.tw/Content_List.aspx?n=20443564F26622DC&topn=D39E2B72B0BDFA15)
- [HPO（官方）](http://www.chinahpo.org/)
- [SNOMED（官方）](http://mall.cnki.net/reference/detail_R200908044.html)
- [SNOMED（非官方）](http://chisc.net/doc/view/5201.html)
- [MeSH（非官方）](http://chisc.net/doc/view/9270.html)

## UMLS机器翻译
- [百度翻译](https://fanyi.baidu.com)
- [谷歌翻译](https://translate.google.cn/)
- [金山词霸](http://www.iciba.com/)

# 运行示例
运行生成`hpo.txt`的代码：

```
cd code
export PYTHONPATH=`pwd`:$PYTHONPATH
python segment/hpo.py
```
## 可能需要安装的python包
```
pip install tqdm
pip install seaborn
pip install xlrd
pip install pip install opencc-python-reimplemented
pip install zhon
```





