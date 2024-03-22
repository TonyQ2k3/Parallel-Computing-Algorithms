# Giải thuật tính toán song song và phân bố
Các giải thuật song song sử dụng trong môn học NT538.O11

# Mục lục

1. [Prefix Sum](#prefix-sum-scan)

2. [Fibonacci](#fibonacci-tham-khảo)

3. [Merge Sort](#merge-sort)

4. [Quick Sort](#quick-sort)

# Nội dung

## Prefix Sum (Scan)
### Ý tưởng
Thuật toán prefix sum song song hoạt động theo nguyên tắc chia để trị, trong đó, mỗi phần tử của mảng đều kèm theo một giá trị gọi là offset, giá trị này đại diện cho tổng của các phần tử trước nó.

Thuật toán này chia mảng ban đầu thành 2 nửa, sau đó nó tính tổng các phần tử của mảng con bên trái và cộng giá trị này vào offset của mỗi phần tử trong mảng con bên phải.

Tiếp tục lặp lại thao tác này trên các mảng con một cách song song đến khi mỗi mảng con tạo ra chỉ còn một phần tử, lúc này thuật toán sẽ cộng giá trị của phần tử đó với offset của nó và đưa vào mảng kết quả.

### Thực hiện
1.	Kiểm tra, nếu mảng chỉ có 1 phần tử thì cộng giá trị phần tử đó với offset của nó và đưa vào vị trí tương ứng trong mảng kết quả, sau đó kết thúc.
Nếu ngược lại, sang bước 2.
2.	Chia mảng thành 2 nửa mảng con.
3.	Tính tổng của mảng con bên trái.
4.	Cộng giá trị tổng này vào offset của mảng bên phải.
5.	Thực hiện đệ quy song song trên mảng con bên trái.
6.	Thực hiện đệ quy song song trên mảng con bên phải.

### Mã giả
```
result = [];

prefix_sum(arr[], left, right, offset) {
    if (left >= right) {
        result[left] = arr[left] + offset;
        return;
    }
    mid = (left + right) / 2;
    leftSum = parallel_sum(arr, left, mid);
    
    IN PARALLEL:
    prefix_sum(arr, left, mid, offset);
    prefix_sum(arr, mid+1, right, offset + leftSum);
}
```

## Fibonacci (tham khảo)
### Ý tưởng
Thuật toán này sử dụng phương pháp chia để trị. Để tính số fibonacci thứ n, thuật toán thực hiện đệ quy song song để tìm số fibonacci thứ n-1 và n-2, sau đó cộng 2 số này lại và trả về kết quả.

### Thực hiện
1. Nếu n nhỏ hơn 2, trả về 1 (base case).
2. Tính fibonacci(n-1) song song.
3. Tính fibonacci(n-2) song song.

### Mã giả
```
fibonacci (n) { 
    if (n <= 2) 
        return 1; 
    else {
        IN PARALLEL:    
        A = fibonacci(n-1);
        B = fibonacci(n-2);
    }
    return A+B;
}
```

## Merge sort
### Ý tưởng
Thuật toán này gồm 2 phần: phần Tách (split) và phần Gộp (merge).

**Thuật toán tách**: 
+ Thuật toán chia mảng thành 2 nửa, rồi tiếp tục chia trên 2 mảng đó đến khi mỗi mảng con tạo ra chỉ còn một phần tử. Sau đó thuật toán sẽ thực hiện thao tác gộp và sắp xếp.

**Thuật toán gộp**: 
+ Thuật toán lấy phần tử giữa nhất (m) của mảng A, đồng thời chia mảng đó thành 2 nửa. 

+ Tiếp đến, nó dùng giải thuật Binary Search để xác định vị trí phù hợp của m bên trong mảng B, rồi chia đôi mảng B tại vị trí đó và chèn m vào. 

+ Sau đó, nó lặp lại thao tác gộp này lên nửa trái của A và nửa trái của B, rồi đến nửa phải của A và nửa phải của B, tiếp tục đến khi tất cả các mảng con được gộp lại.

### Thực hiện
1. Kiểm tra, nếu mảng chỉ có 1 phần tử thì kết thúc, nếu ngược lại đến bước 2.
2. Lấy mid làm vị trí chính giữa mảng.
3. Thực hiện đệ quy song song lên mảng con bên trái.
4. Thực hiện đệ quy song song lên mảng con bên phải.
5. Thực hiện gộp mảng con bên trái và mảng con bên phải một các song song.

   1. Kiểm tra, nếu một trong hai mảng rỗng, đưa các phần tử trong mảng còn lại vào mảng kết quả C.
   2. Chọn m là vị trí giữa nhất trong mảng A (giá trị của nó tạm gọi là median của A).
   3. Dùng giải thuật binary_search để tìm ra vị trí phù hợp của median trong mảng B. Giải thuật này tìm kiếm phần tử lớn nhất nhỏ hơn median, và trả về vị trí của nó. Nếu không thể tìm thấy phần tử nào nhỏ hơn, nó trả về vị trí đầu tiên của mảng B trừ đi 1.
   4. Đưa median của A vào vị trí phù hợp trong C.

### Mã giả
```
C = [];

parallel_merge_sort(arr, left, right) {
    if (left >= right)
        return;
    mid = (right + left) / 2;
    
    IN PARALLEL:
    parallel_merge_sort(arr, left, mid);
    parallel_merge_sort(arr, mid+1, right);

    parallel_merge(arr, left, mid, mid+1, right, C, left);
}

parallel_merge(arr, left_A, right_A, left_B, right_B, C, offset_C) {
    if (left_A > right_A) {
        for (i = left_B; i <= right_B; i++) {
            C[offset_C + (i - left_B)] = arr[i];
        }
        return;
    }
    if (left_B > right_B) {
        for (i = left_A; i <= right_A; i++) {
            C[offset_C + (i - left_A)] = arr[i];
        }
        return;
    }
    m = (right_A + left_A) / 2;
    pos_B = binary_search(arr, left_B, right_B, arr[m]);

    pos_C = (m - left_A) + (pos_B - left_B) + 1;
    C[pos_C + offset_C] = arr[m];
    
    IN PARALLEL:
    parallel_merge(arr, left_A, m-1, left_B, pos_B, C, offset_C);
    parallel_merge(arr, m+1, right_A, pos_B+1, right_B, C, offset_C + pos_C + 1);
}
```

## Quick Sort
### Ý tưởng
Đầu tiên, ta lấy phần tử giữa nhất của mảng làm pivot (trục chốt). 

Tiếp theo, sử dụng giải thuật lọc và đóng gói (filtering/packing) lên mảng để phân chia mảng dựa trên trục chốt, đồng thời xác định được vị trí của trục chốt trong mảng đã sắp xếp. 

Sau đó, trục chốt được đưa vào đúng vị trí trong mảng, những phần tử nhỏ hơn hoặc bằng nó được đẩy về phía bên trái, những phần tử lớn hơn được đưa về phía bên phải.

Giải thuật sẽ tiếp tục đệ quy song song lên mảng con bên trái và mảng con bên phải đến khi tất cả các phần tử đều đã được sắp xếp và mảng ko thể chia đôi được nữa.

### Thực hiện
1.	Kiểm tra, nếu mảng chỉ còn một phần tử thì kết thúc giải thuật, nếu ngược lại thì đến bước 2.
2.	Chọn giá trị giữa nhất của mảng làm pivot.
3.	Dùng giải thuật filter_less() lên mảng để lọc ra những phần tử nhỏ hơn hoặc bằng pivot và cho vào mảng L. Đồng thời, dùng giải thuật filter_more() lên mảng để lọc ra những phần tử lớn hơn pivot và cho vào mảng R.
4.	Lần lượt đưa các phần tử trong L vào mảng, sau đó đến pivot, rồi đến các phần tử trong mảng R.
5.	Đệ quy song song lên nửa bên trái (mảng L).
6.	Đệ quy song song lên nửa bên phải (mảng R).

### Mã giả
```
C = [];

parallel_partition(arr, left, right) {
    pivot = arr[(right - left) / 2];
    L = [];
    R = [];
    parallel_filter_less(arr, pivot, L);
    parallel_filter_more(arr, pivot, R);
    
    for (i = 0; i < L.length; i++) {
        arr[i] = L[i];
    }
    arr[L.length] = pivot;
    for (i = 0; i < R.length; i++) {
        arr[i + R.length + 1] = R[i];
    }
    return L.length;
}

parallel_quick_sort(arr, left, right) {
    if (left >= right)
        return;

    pivot = parallel_partition(arr, left, right);
    
    IN PARALLEL:
    parallel_quick_sort(arr, left, pivot-1);
    parallel_quick_sort(arr, pivot+1, right);
}

parallel_filter_less(arr, pivot, L) {
    for(i = 0; i < arr.length; i++) {
        if (arr[i] <= pivot)
            S[i] = 1;
    }
    pos = parallel_scan(S);
    for (i = 0; i < arr.length; i++) {
        if (S[i] == 1) 
            L[pos[i]-1] = arr[i];
    }
}

parallel_filter_more(arr, pivot, L) {
    for(i = 0; i < arr.length; i++) {
        if (arr[i] <= pivot)
            S[i] = 1;
    }
    pos = parallel_scan(S);
    for (i = 0; i < arr.length; i++) {
        if (S[i] == 1) 
            L[pos[i]-1] = arr[i];
    }
}
```
