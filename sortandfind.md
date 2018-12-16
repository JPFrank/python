### 排序+查找算法总结(Python+Java(Java代码后续补充)篇)
排序算法大致有如下几种（数据存放于内存中):<br />
总结如图所示：<br />
![Image discription](https://github.com/JPFrank/image/blob/master/%E6%8E%92%E5%BA%8F.png)
  
  1. 直接插入排序 
  2. 希尔排序
  3. 选择排序
  4. 堆排序
  5. 冒泡排序
  6. 快速排序
  7. 归并排序
  8. 基数排序
  
直接插入排序
  首先介绍直接插入排序，直接上直接插入排序的代码
  Python代码如下：
  ```
  def insertSort(array):
      for i in range(len(array)):
          for j in range(i):
              if array[i] < array[j]:
                  array.insert(j, array.pop(i))
                  break
      return array

  array = insertSort([3,2,6,9,8])
  print(array)
  ```

  每次外层循环之后，都会得到对应长度的有序数组；灵活使用下标进行插入删除。
  数组定长的情况下，扣除错误位置的值，插入正确的地方。
  其实对直接插入排序可以这么理解，无序的数组可以看作无序的牌堆，然后手上的牌组可视为已有有序数组，每次抓牌并插入手牌排好序的过程可以看作插入排序中对一个   元素操作的动作。其实代码中只用到了一个数组，理解起来可以当作两个数组，这样更清楚一点。

希尔排序
```
def shell_sort(slist):
    gap = len(slist)
    while gap > 1:
        gap = gap // 2
        for i in range(gap, len(slist)):
            for j in range(i % gap, i, gap):
                if slist[i] < slist[j]:
                    slist[i], slist[j] = slist[j], slist[i]
    return slist
 
slist = shell_sort([4,5,6,7,3,2,6,9,8])
print slist
```

