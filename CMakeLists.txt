cmake_minimum_required(VERSION 3.2)
project(src/pyjion)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(BUILD_TESTS "Build the unit tests" OFF)

include(CMakeOptimizations.txt)

if (UNIX AND NOT APPLE)
    message(STATUS "Enabling PIC")
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fpic")
endif()

if (SKBUILD)
    find_package(PythonExtensions REQUIRED)
    message(STATUS "Using Python libraries for skbuild " ${PYTHON_LIBRARIES})
    message(STATUS "Using Python headers for skbuild " ${PYTHON_INCLUDE_DIRS})
endif (SKBUILD)

if (NOT PYTHON_LIBRARIES)
    find_package (Python3 3.9 COMPONENTS Interpreter Development)
else()
    set(Python3_LIBRARIES ${PYTHON_LIBRARIES})
    set(Python3_INCLUDE_DIRS ${PYTHON_INCLUDE_DIRS})
endif()

message(STATUS "Using Python libraries " ${Python3_LIBRARIES})
message(STATUS "Using Python headers " ${Python3_INCLUDE_DIRS})

include_directories(${Python3_INCLUDE_DIRS})

set (CLR_DIR CoreCLR/src/coreclr)

add_definitions(-DUSE_STL)

IF(CMAKE_BUILD_TYPE MATCHES Debug)
    message(STATUS "Enabling verbose messages")
    add_definitions(-DDEBUG)
    set(BUILD_TESTS ON)
ENDIF(CMAKE_BUILD_TYPE MATCHES Debug)

if(DUMP_JIT_TRACES)
    message(STATUS "Enabling very-very-verbose messages")
    add_definitions(-DDUMP_JIT_TRACES)
endif()

if(NOT WIN32)
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
    include_directories(CoreCLR/src/coreclr/src/pal/inc/rt CoreCLR/src/coreclr/src/pal/inc CoreCLR/src/coreclr/src/pal/prebuilt/inc)
    add_compile_options(-DPAL_STDCPP_COMPAT)
    add_compile_options(-fexceptions)
    add_compile_options(-fvisibility=hidden)

    add_definitions(-DTARGET_UNIX)
    message(STATUS "Enabling UNIX Patches")
    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        add_compile_options(-Wno-null-arithmetic)
    else(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        add_compile_options(-Wno-conversion-null -Wno-pointer-arith)
    endif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
else()
    add_definitions(-DWINDOWS=1)
    add_definitions(-D_HAS_STD_BYTE=0)
    if (MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++latest")
        set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /STACK:80000000")
    endif(MSVC)
endif(NOT WIN32)


add_definitions(-DPROFILING_SUPPORTED -DUNICODE)

if (${CMAKE_SYSTEM_PROCESSOR} STREQUAL "x86_64")
    set(IS_64 1)
elseif (${CMAKE_SYSTEM_PROCESSOR} STREQUAL "amd64")
    set(IS_64 1)
elseif (${CMAKE_SYSTEM_PROCESSOR} STREQUAL "AMD64")
    if (CMAKE_CL_64)
        set(IS_64 1)
    endif()
else()
    message(STATUS "Don't recognise CPU arch " ${CMAKE_SYSTEM_PROCESSOR})
endif()

if (IS_64)
    add_definitions(-D_TARGET_AMD64_)
    add_definitions(-DTARGET_AMD64)
    add_definitions(-DTARGET_64BIT)
    add_definitions(-DHOST_64BIT)
    add_definitions(-DHOST_AMD64)
    message(STATUS "Enabling AMD64")
    if (NOT WIN32)
        add_definitions(-DUNIX_AMD64_ABI)
        add_definitions(-DUNIX_AMD64_ABI_ITF)
        message(STATUS "Enabling AMD64 ABI")
    endif()
else()
    add_definitions(-DTARGET_X86)
    add_definitions(-D_TARGET_X86_)
    message(STATUS "Enabling x86")
endif()

include_directories(CoreCLR/src/coreclr/src/inc CoreCLR/src/coreclr/src/jit)

if (UNIX)
    if(DEFINED ENV{DOTNET_ROOT})
        file(GLOB DOTNETPATH $ENV{DOTNET_ROOT}/shared/Microsoft.NETCore.App*/5.*/)
    else()
        file(GLOB DOTNETPATH /usr/local/share/dotnet/shared/Microsoft.NETCore.App*/5.*/)
        if (DOTNETPATH STREQUAL "")
            file(GLOB DOTNETPATH /usr/share/dotnet/shared/Microsoft.NETCore.App*/5.*/)
        endif()
    endif()
    if (DOTNETPATH STREQUAL "")
        message(FATAL_ERROR "Cant locate .NET 5")
    endif()
    message(STATUS "Found .NET 5 in " ${DOTNETPATH})
endif()

if (WIN32)
    set(CLR_OS_BUILD Windows_NT.x64.Debug)
    if(DEFINED ENV{DOTNET_ROOT})
        file(GLOB DOTNETPATH $ENV{DOTNET_ROOT}/shared/Microsoft.NETCore.App*/5.*/)
    else()
        file(GLOB DOTNETPATH $ENV{LOCALAPPDATA}/Microsoft/dotnet/shared/Microsoft.NETCore.App*/5.*/)
    endif()
    if (DOTNETPATH STREQUAL "")
        message(FATAL_ERROR "Cant locate .NET 5")
    endif()
    message(STATUS "Found .NET 5 in " ${DOTNETPATH})
endif()

add_definitions(-DGIL)  # use Python GIL on sub function calls

if (UNIX AND NOT APPLE)
    set(CLR_OS_BUILD Linux.x64.Debug)
    set(CLR_JIT_LIB "libclrjit.so")
    set(CLR_CMAKE_HOST_UNIX 1)
    add_definitions(-DFEATURE_SIMD)
    add_definitions(-DFEATURE_HW_INTRINSICS)
    add_compile_options(-fPIC)
    add_definitions(-DINDIRECT_HELPERS)
endif()

if (APPLE)
    set(CLR_OS_BUILD OSX.x64.Debug)
    include_directories(src/pyjion/compat)
    set(CLR_CMAKE_HOST_UNIX 1)
    set(CLR_JIT_LIB "libclrjit.dylib")
    add_definitions(-D_XOPEN_SOURCE)
    add_definitions(-DTARGET_OSX)
    add_compile_options(-fdeclspec)
    add_definitions(-DFEATURE_SIMD)
    add_definitions(-DFEATURE_HW_INTRINSICS)
endif()

if(NET_SRC_LIB)  # use the libraries compiled from source
    set(DOTNETPATH ${CMAKE_SOURCE_DIR}/CoreCLR/artifacts/bin/coreclr/${CLR_OS_BUILD})
endif()

set(SOURCES src/pyjion/absint.cpp src/pyjion/absvalue.cpp src/pyjion/intrins.cpp src/pyjion/jitinit.cpp src/pyjion/pycomp.cpp src/pyjion/pyjit.cpp src/pyjion/exceptionhandling.cpp src/pyjion/stack.cpp src/pyjion/block.cpp)

if (WIN32)
    enable_language(ASM_MASM)
    add_definitions(-DINDIRECT_HELPERS)
    if (IS_64)
        set(HOST_ASM_MASM_X86_64 true)
    endif()
    set(SOURCES ${SOURCES} src/pyjion/helpers.asm)
else()
    enable_language(ASM)
    set(SOURCES ${SOURCES} src/pyjion/helpers.S)
endif()

add_library(pyjionlib OBJECT ${SOURCES})
add_library(_pyjion MODULE $<TARGET_OBJECTS:pyjionlib>)

if (WIN32)
    add_custom_command(
        TARGET _pyjion POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        ${DOTNETPATH}/clrjit.dll
        ${CMAKE_CURRENT_BINARY_DIR}/clrjit.dll
    )
endif(WIN32)

set_target_properties(
        _pyjion
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_pyjion"
        LINKER_LANGUAGE C
)

if (NOT SKBUILD)
    target_link_libraries(_pyjion ${Python3_LIBRARIES})
endif()

if (BUILD_TESTS)
    # Testing
    add_subdirectory(Tests/Catch)
    set(TEST_SOURCES Tests/testing_util.cpp Tests/test_basics.cpp Tests/test_compiler.cpp Tests/test_absint.cpp Tests/Tests.cpp Tests/test_wrappers.cpp Tests/test_exceptions.cpp Tests/test_scopes.cpp Tests/test_tracing.cpp)
    add_executable(unit_tests ${TEST_SOURCES} $<TARGET_OBJECTS:pyjionlib>)
    if (NOT WIN32)
        set_property(TARGET unit_tests PROPERTY CXX_STANDARD 17)
        set_property(TARGET unit_tests PROPERTY CXX_EXTENSIONS OFF)
    endif(NOT WIN32)
    target_include_directories(unit_tests PRIVATE src/pyjion)
    target_link_libraries(unit_tests Catch2::Catch2)
    target_link_libraries(unit_tests ${Python3_LIBRARIES})

    if (NOT WIN32)
        target_link_libraries(unit_tests ${DOTNETPATH}/${CLR_JIT_LIB})
    endif()
endif(BUILD_TESTS)

# Code Coverage Configuration
add_library(coverage_config INTERFACE)

option(CODE_COVERAGE "Enable coverage reporting" OFF)
if(CODE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # Add required flags (GCC & LLVM/Clang)
    target_compile_options(coverage_config INTERFACE
            -O0        # no optimization
            -g         # generate debug info
            --coverage # sets all required flags
            )
    target_link_options(coverage_config INTERFACE --coverage)
endif(CODE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")

if (NOT WIN32)
    target_link_libraries(_pyjion ${DOTNETPATH}/${CLR_JIT_LIB})
endif()

if (SKBUILD)
    python_extension_module(_pyjion)
endif (SKBUILD)

install(TARGETS _pyjion LIBRARY DESTINATION src/pyjion)