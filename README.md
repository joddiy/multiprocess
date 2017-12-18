# Python 通用多进程模型

## 使用方法

### 调用方式

入口方法

```python
# 引入 多进程模型 和 消息模型
from src.components.multiprocess.InfoTask import InfoTask
from src.components.multiprocess.MultiProcess import MultiProcess

if __name__ == '__main__':
    # 实例化多进程模型（指定进程池大小）
    mp = MultiProcess(10)
    # 开启多进程模型
    mp.start()
    for i in range(10):
        # 新建消息实例（指定任务 module，超时时间，参数）
        task = InfoTask("src.components.multiprocess.example.Demo", 1, (i, i))
        # 向进程池推送消息
        mp.push(task)
    # 不再发送新的任务，等待所有任务退出
    mp.stop()
```
### 任务 module
需要交给进程池去完成的 module，包含三个部分：runnable，callback，error_callback

```python
def runnable(*args):
    """
    交给 worker 执行的方法
    :param args:
    :return:
    """
    pass


def callback(*result):
    """
    执行成功后的调用
    :param result:
    :return:
    """
    pass


def error_callback(error):
    """
    执行失败后的调用
    :param error:
    :return:
    """
    pass

```

## 架构和设计

### 架构图

![架构图](asset/structure.png)

### 组成部分

#### 任务 *Task*

任务由父进程 *1* 通过管道推送给子进程 *2*，其中指定了任务模块所在命名空间 *module*（其中需要包含 *runnable，callback 和 error_callback*）三个方法，该任务的超时时间 &*Timeout*，和需要传递给 runnable 方法的参数 *Args*。


#### 父进程 *1*

即入口进程，与调用入口在统一进程，负责开启模块，在开启的同时，指定允许的进程池容量，父进程通过管道 *Pipe* 向子进程 *2* 推送任务消息。

#### 子进程 *2*

即调度进程，该进程维护了一个进程池 *Process Pool*，并通过管道 *Pipe* 和父进程 *1* 通讯，如果接收到了父进程 *1* 推送的任务，就分配给进程池 *Process Pool* 去执行，如果接收到退出消息，就等待进程池 *Process Pool* 中所有的进程退出后退出。

#### 进程池 *Process Pool*

其容量在父进程 *1* 开启模块时指定，采用带 callback 和 error_callback 的异步执行模式。

#### 任务进程 *3-7*

真正执行任务的 Worker 进程，采用 **双线程模式**，一个线程 *Thread1* 执行任务，另一个线程 *Thread2* 负责监控超时。如果任务成功，则返回结果并通知**子进程2**调用 callback 方法，如果超时或者出错，通知**子进程2**调用 error_callback 方法


### 设计思想

#### 线程 OR 进程

Python 的线程由于 Global Interpreter Lock（GIL，全局解释锁）的存在，使其实际上只能串行工作。另外，线程由于共享内存空间，会存在并行不安全性的问题。相反，进程是真正意义上的并发执行，且进程与进程之间是隔离的，不共享内存空间，因此一个进程崩溃并不会影响其他进程。

#### 由子进程维护进程池

为了实现解耦，不是由父进程直接维护进程池，而是新建一个子进程来维护，父进程只需要将消息通过管道推送给子进程即可。


#### 分配任务

子进程分配任务给进程池中的进程时，采用的是非阻塞的方式，即消息一旦推送给子进程，子进程就会立刻将任务分配给进程池（如果进程池有空闲的话）。在这种模式下，接收一个任务就会立即执行一个任务，能够提高效率。

#### 双线程监督超时

为了避免进程池中的进程出现假死而一直无法退出的情况，对于所有任务，当分配给它一个进程的时候，都会采用双线程的方式执行，一个线程用于执行任务，另一个线程用于监督是否超时，如果超时就会杀死任务并回调。

#### 带有正常和异常的回调

任务支持指定正常和异常回调函数，当函数正常退出时，会由子进程调用正常回调函数，当超时或者异常退出时，会由子进程调用异常回调函数。因此可以对任务的执行进行监控和后续操作。

### 注意

**一定要 catch 掉【正常回调】和【异常回调】抛出的异常**，否则父进程会无法退出。

