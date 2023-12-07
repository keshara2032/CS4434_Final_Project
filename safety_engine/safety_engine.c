#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>

#define PORT 9999
#define BUFFER_SIZE 1024
#define TIMEOUT_SECONDS 1 // Timeout in seconds
#define TIMEOUT_uSECONDS 0 // Timeout in seconds

int main() {
    int sockfd;
    struct sockaddr_in serverAddr;
    socklen_t addr_size;
    char buffer[BUFFER_SIZE];

    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Error in socket creation");
        exit(EXIT_FAILURE);
    }

    memset(&serverAddr, '\0', sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    // Bind socket to port
    if (bind(sockfd, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    struct timeval timeout;
    timeout.tv_sec = TIMEOUT_SECONDS;
    timeout.tv_usec = TIMEOUT_uSECONDS;

    // Set receive timeout
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char *)&timeout, sizeof(timeout)) < 0) {
        perror("Error setting socket options");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d with a timeout of %d seconds...\n", PORT, TIMEOUT_SECONDS);

    int old_sequence = 0;
    while (1) {
        addr_size = sizeof(serverAddr);
        memset(buffer, '\0', sizeof(buffer));

        // Receive packet
        ssize_t bytesReceived = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&serverAddr, &addr_size);
        if (bytesReceived < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                printf("Receive timeout. No data received within the timeout period.\n");
            } else {
                perror("Error in receiving data");
            }
        } else {
            // Display received packet
            printf("Received message: %s\n", buffer);
                // Convert string to integer using atoi()
            int new_sequence = atoi(buffer);
            
            printf("Converted integer: %d\n", new_sequence);

            if(new_sequence == old_sequence+1){
                printf("Correct sequence received!\n");
                old_sequence = new_sequence;
            }else{
                printf("Incorrect sequence received!\n");
            }
   
        }
    }

    close(sockfd);
    return 0;
}
