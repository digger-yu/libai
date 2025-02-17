# coding=utf-8
# Copyright 2021 The OneFlow Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random

import oneflow as flow
from oneflow.utils.data import Dataset

from libai.data.structures import DistTensorData, Instance


def pad_right(data, pad_id=0, max_len=1350):
    n = max_len - data.shape[0]
    return flow.cat((data, flow.full((n,), pad_id, dtype=data.dtype)))


class AlpacaDataset(Dataset):
    def __init__(self, path, tokenizer, max_len=1350):
        self.data = flow.load(path)
        random.shuffle(self.data)
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        input_ids = pad_right(self.data[index]["input_ids"], pad_id=0, max_len=self.max_len)
        labels = pad_right(self.data[index]["labels"], pad_id=-1, max_len=self.max_len)

        return Instance(
            input_ids=DistTensorData(input_ids),
            labels=DistTensorData(labels),
        )
