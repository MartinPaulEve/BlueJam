#About BlueJam
BlueJam is a digital preservation system for open-access scholarly material. It is licensed under the GPL version 3.0.

BlueJam is designed to be simple to setup and configure. The software will be distributed in a form that will make it easy for new clients to join the main international network. BlueJam can also be run as a separate, segmented network, although for simplicity it operates on a "no security" model and only handles open-access, openly licensed material.

BlueJam is currently in active development and is not yet ready for production use.

#Architecture
BlueJam operates on a server/client model with peer to peer replication and validation planned. Initial replication consists of a single serialized database clone operation followed by a distributed file download process.

The BlueJam server hub ingests content from its source list. Upon discovering new content, the server raises an event on a client, instructing the client to fetch the new material from the server. The server then works through the list of known clients, coordinating transfers between them to minimize server load.

Each BlueJam server has a list of known clients. These clients are regularly pinged for uptime and files are arbitrarily downloaded by other clients to perform CRC comparisons to ensure data integrity. 

#Readiness
BlueJam is _not_ ready for production. It is in early stage development. It will be ready when it is done.