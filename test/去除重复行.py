#!/usr/bin/env python
line_set = set()
with open('input.txt', 'r', encoding='utf8') as input_f:
    with open('output.txt', 'a', encoding='utf8') as output_f:
        for line in input_f:
            if line not in line_set:
                line_set.add(line)
                output_f.write(line)
            else:
                # 打印重复行
                print(line)
