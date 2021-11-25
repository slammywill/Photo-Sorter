def child_indices_16_heap(parent):
    return [16*parent + i + 1 for i in range(16)]

print(child_indices_16_heap(16))