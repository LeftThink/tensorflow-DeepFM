
#-*- coding: utf-8 -*-
"""
A data parser for Porto Seguro's Safe Driver Prediction competition's dataset.
URL: https://www.kaggle.com/c/porto-seguro-safe-driver-prediction
"""
import pandas as pd


class FeatureDictionary(object):
    def __init__(self, trainfile=None, testfile=None,
                 dfTrain=None, dfTest=None, numeric_cols=[], ignore_cols=[]):
        assert not ((trainfile is None) and (dfTrain is None)), "trainfile or dfTrain at least one is set"
        assert not ((trainfile is not None) and (dfTrain is not None)), "only one can be set"
        assert not ((testfile is None) and (dfTest is None)), "testfile or dfTest at least one is set"
        assert not ((testfile is not None) and (dfTest is not None)), "only one can be set"
        self.trainfile = trainfile
        self.testfile = testfile
        self.dfTrain = dfTrain
        self.dfTest = dfTest
        self.numeric_cols = numeric_cols
        self.ignore_cols = ignore_cols
        self.gen_feat_dict()

    def gen_feat_dict(self):
        if self.dfTrain is None:
            dfTrain = pd.read_csv(self.trainfile)
        else:
            dfTrain = self.dfTrain
        if self.dfTest is None:
            dfTest = pd.read_csv(self.testfile)
        else:
            dfTest = self.dfTest

        #将训练和测试集做一下拼接
        df = pd.concat([dfTrain, dfTest]) 
        self.feat_dict = {}
        tc = 0
        for col in df.columns:
            if col in self.ignore_cols:
                continue
            if col in self.numeric_cols:
                # map to a single index
                # 对于数值型特征只映射到一个index
                self.feat_dict[col] = tc
                tc += 1
            else:
                #对于类别性特征,根据类别数对就到c个索引
                us = df[col].unique()
                self.feat_dict[col] = dict(zip(us, range(tc, len(us)+tc)))
                tc += len(us)
        """
        tc, ex:
        {
            'fe1': 0, #因为是数值型特征
            'fe2': {  #因为是类别型特征,而且有3个类别
                'c21': 1,
                'c22': 2,
                'c23': 3
            },
            ...
        }
        """
        self.feat_dim = tc


class DataParser(object):
    def __init__(self, feat_dict):
        self.feat_dict = feat_dict

    def parse(self, infile=None, df=None, has_label=False):
        assert not ((infile is None) and (df is None)), "infile or df at least one is set"
        assert not ((infile is not None) and (df is not None)), "only one can be set"

        if infile is None:
            dfi = df.copy() #注意这里做了一个拷贝
        else:
            dfi = pd.read_csv(infile)
        if has_label:
            #y = dfi["target"].values.tolist()
            #dfi.drop(["id", "target"], axis=1, inplace=True)
            y = dfi["click"].values.tolist()
            dfi.drop(["id", "click"], axis=1, inplace=True)
        else:
            ids = dfi["id"].values.tolist()
            dfi.drop(["id"], axis=1, inplace=True)
        # dfi for feature index
        # dfv for feature value which can be either binary (1/0) or float (e.g., 10.24)
        dfv = dfi.copy() #真是不惜内存啊,就你这两个拷贝我还跑个毛啊
        for col in dfi.columns:
            if col in self.feat_dict.ignore_cols:
                #要忽略的特征直接丢弃
                dfi.drop(col, axis=1, inplace=True)
                dfv.drop(col, axis=1, inplace=True)
                continue
            if col in self.feat_dict.numeric_cols:
                #数值型特征直接相当于直接编码为訪特征对应的一个固定的索引
                dfi[col] = self.feat_dict.feat_dict[col]
            else:
                #类别型特征做一个映射,因为每个类别会对应到一个不同的索引
                dfi[col] = dfi[col].map(self.feat_dict.feat_dict[col])
                dfv[col] = 1. #类别型特征设为1,数值型特征仍然为原始值

        # list of list of feature indices of each sample in the dataset
        Xi = dfi.values.tolist() #变成了一个MxN的list
        # list of list of feature values of each sample in the dataset
        Xv = dfv.values.tolist()
        if has_label:
            return Xi, Xv, y
        else:
            return Xi, Xv, ids

