cmake_minimum_required(VERSION 3.10)

project(websockets_example)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find and link Boost libraries
find_package(Boost REQUIRED COMPONENTS system thread)
if (NOT Boost_FOUND)
    message(FATAL_ERROR "Boost libraries not found!")
endif()

include(FetchContent)
FetchContent_Declare(
    json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.3
)
FetchContent_MakeAvailable(json)

# Add executable
add_executable(server web_sockets.cpp)

# Link Boost libraries
target_link_libraries(server PRIVATE nlohmann_json::nlohmann_json Boost::system Boost::thread pthread)

# Include Boost headers
target_include_directories(server PRIVATE ${Boost_INCLUDE_DIRS})