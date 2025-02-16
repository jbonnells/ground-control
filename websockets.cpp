#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/strand.hpp>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <chrono>

using namespace boost::asio;
using namespace boost::beast;
using namespace boost::asio::ip;
using json = nlohmann::json;

class WebSocketSession : public std::enable_shared_from_this<WebSocketSession>
{
    websocket::stream<tcp::socket> ws_;

    // use the io_context's executor type for the strand
    boost::asio::strand<boost::asio::io_context::executor_type> strand_;

public:
    explicit WebSocketSession(tcp::socket socket)
        : ws_(std::move(socket)),
          strand_(boost::asio::make_strand(
              *static_cast<boost::asio::io_context *>(&(ws_.get_executor().context()))))
    {
    }

    void start()
    {
        std::cout << "start" << std::endl;
        ws_.async_accept(
            boost::asio::bind_executor(strand_,
                                       std::bind(&WebSocketSession::on_accept, shared_from_this(), std::placeholders::_1)));
    }

private:
    void on_accept(boost::system::error_code ec)
    {
        std::cout << "on_accept" << std::endl;
        if (ec)
            return fail(ec, "accept");
        send_telemetry();
    }

    void send_telemetry()
    {
        std::cout << "send_telemetry" << std::endl;
        json telemetryData = {
            {"altitude", 1000 + rand() % 1000},
            {"speed", 500 + rand() % 500},
            {"heading", rand() % 360}};

        ws_.async_write(
            boost::asio::buffer(telemetryData.dump()),
            boost::asio::bind_executor(strand_,
                                       std::bind(&WebSocketSession::on_write, shared_from_this(),
                                                 std::placeholders::_1, std::placeholders::_2)));
    }

    void on_write(boost::system::error_code ec, std::size_t /*bytes_transferred*/)
    {
        std::cout << "on_write" << std::endl;
        if (ec)
            return fail(ec, "write");
        std::this_thread::sleep_for(std::chrono::seconds(1));
        send_telemetry();
    }

    void fail(boost::system::error_code ec, char const *what)
    {
        std::cerr << what << ": " << ec.message() << "\n";
    }
};

class WebSocketServer
{
    tcp::acceptor acceptor_;
    tcp::socket socket_;

public:
    WebSocketServer(io_context &ioc, tcp::endpoint endpoint)
        : acceptor_(ioc, endpoint), socket_(ioc)
    {
        do_accept();
    }

private:
    void do_accept()
    {
        acceptor_.async_accept(socket_,
                               [this](boost::system::error_code ec)
                               {
                                   if (!ec)
                                       std::make_shared<WebSocketSession>(std::move(socket_))->start();
                                   do_accept();
                               });
    }
};

int main()
{
    try
    {
        io_context ioc{1};
        tcp::endpoint endpoint{tcp::v4(), 4000};
        WebSocketServer server(ioc, endpoint);
        std::cout << "WebSocket server running on ws://localhost:4000" << std::endl;
        ioc.run();
    }
    catch (std::exception &e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
}
