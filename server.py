import asyncio

list_of_users = []


async def handle_echo(reader, writer):
    list_of_users.append(writer)
    addr = writer.get_extra_info('peername')
    while True:
        data = await reader.read(1024)
        message = data.decode()
        if not message:
            print(f'Client {addr} disconnected!')
            list_of_users.remove(writer)
            break
        msg(message)
        print(f'Recieved message:{message!r}')


def msg(message):
    for user in list_of_users:
        user.write(message.encode())


async def main():
    server = await asyncio.start_server(
        handle_echo, '0.0.0.0', 8886)
    addr = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Client {addr} connected.')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
