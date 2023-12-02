def read_input():
    lines: [str] = []
    with open('./data/day_1-data.txt', 'r') as f:
        lines = f.readlines()

    return lines

def main():
    lines: [str] = read_input()

    sum_: int = 0
    for line in lines:
        filtered_line = list(filter(lambda _line: _line.isnumeric(), line))
        num_1, num_2 = int(filtered_line[0]), int(filtered_line[-1])
        
        sum_ += num_1 * 10 + num_2
        
    
    return sum_

if __name__ == "__main__":
    print(main())