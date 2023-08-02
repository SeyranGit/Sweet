# Sweet
```
use os;
use sys;

name = 'Sweet';
nikname = "sw";
age = 0;

func getName(name_id, global_id) {
    count = 0;
    loop {
        count = 1;
        if (count == 1 and name_id == 0 or global_id == 0) {
            count_1 = 1000;
            count_2 = 1000;
            count_3 = 1000;
            count_4 = 1000;
            count_5 = 1000;
            brake;
        }
    }
    
    if (count_1 != 1000) {
        func counter() { loop {} }
    }
}

```
The project is not finished yet!

# While the program still outputs:
```
{
  using: {'sys', 'os'}
  name: {
    value: 'Sweet'
    type: string
  }
  nikname: {
    value: "sw"
    type: string
  }
  age: {
    value: 0
    type: int
  }
  getName: {
    type: function
    args:  name_id, global_id
    block: {
      count: {
        value: 0
        type: int
      }
      loop_0: {
        block: {
          count: {
            value: 1
            type: int
          }
          coundition_0: {
            block: {
              count_1: {
                value: 1000
                type: int
              }
              count_2: {
                value: 1000
                type: int
              }
              count_3: {
                value: 1000
                type: int
              }
              count_4: {
                value: 1000
                type: int
              }
              count_5: {
                value: 1000
                type: int
              }
            }
            conds: ('and', [(None, ' count  ==  1'), ('or', [(None, 'name_id  ==  0'), (None, 'global_id  ==  0')])])
          }
        }
      }
      coundition_1: {
        block: {
          counter: {
            type: function
            args:
            block: {
              loop_1: {
                block: {
                }
              }
            }
          }
        }
        conds: (None, ' count_1  !=  1000')
      }
    }
  }
}
```
