---
description: Run NFT Standards and Marketplace Integration Check
globs: ['**/nft/**/*.ts', '**/marketplace/**/*.ts', '**/metadata/**/*.ts', '**/erc721/**/*.sol']
---

# Web3: NFT Standards & Marketplace Integration

<audit_rules>

- You MUST implement proper ERC-721 or ERC-1155 standards for NFT contracts.
- You MUST ensure proper metadata standards following ERC-721 Metadata or OpenSea standards.
- You MUST implement proper royalty standards using EIP-2981 for creator compensation.
- You MUST configure proper access control for minting and transfer operations.
- You MUST implement proper gas optimization for batch operations like minting multiple NFTs.
- You MUST ensure proper IPFS integration for decentralized metadata storage.
- You MUST implement proper marketplace integration with standardized listing and trading interfaces.
- You MUST configure proper event logging for transparency and off-chain indexing.
- You MUST implement proper rarity and attribute validation for NFT collections.
- You MUST ensure proper security against common NFT vulnerabilities like reentrancy and approval exploits.
  </audit_rules>

<example_good>

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

// EIP-2981 NFT Royalty Standard
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract AdvancedNFT is ERC721, ERC721URIStorage, AccessControl, ReentrancyGuard, Pausable, ERC2981 {
    using Counters for Counters.Counter;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    Counters.Counter private _tokenIdCounter;

    // Royalty configuration
    address private _royaltyRecipient;
    uint256 private _royaltyBps; // Basis points (100 = 1%)

    // Collection configuration
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.1 ether;
    uint256 public constant MAX_MINT_PER_TX = 10;
    uint256 public constant MAX_MINT_PER_ADDRESS = 50;

    // Metadata configuration
    string private _baseTokenURI;
    string private _contractURI;

    // Mint tracking
    mapping(address => uint256) public mintedByAddress;

    // Rarity and attributes
    mapping(uint256 => uint256) public rarity;
    mapping(uint256 => mapping(string => string)) public attributes;

    event NFTMinted(address indexed to, uint256 indexed tokenId, uint256 rarity);
    event RoyaltySet(address recipient, uint256 bps);
    event BaseURIUpdated(string newBaseURI);

    constructor(
        string memory name,
        string memory symbol,
        string memory baseTokenURI,
        address royaltyRecipient,
        uint256 royaltyBps
    ) ERC721(name, symbol) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);

        _baseTokenURI = baseTokenURI;
        _royaltyRecipient = royaltyRecipient;
        _royaltyBps = royaltyBps;
    }

    function mint(uint256 quantity)
        external
        payable
        nonReentrant
        whenNotPaused
    {
        require(quantity > 0 && quantity <= MAX_MINT_PER_TX, "Invalid quantity");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");
        require(_tokenIdCounter.current() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(mintedByAddress[msg.sender] + quantity <= MAX_MINT_PER_ADDRESS, "Exceeds per address limit");

        for (uint256 i = 0; i < quantity; i++) {
            _tokenIdCounter.increment();
            uint256 tokenId = _tokenIdCounter.current();

            // Generate random rarity
            uint256 randomRarity = _generateRarity(tokenId);
            rarity[tokenId] = randomRarity;

            // Generate attributes based on rarity
            _generateAttributes(tokenId, randomRarity);

            _safeMint(msg.sender, tokenId);
            emit NFTMinted(msg.sender, tokenId, randomRarity);
        }

        mintedByAddress[msg.sender] += quantity;
    }

    function adminMint(address to, uint256 quantity, uint256 rarityLevel)
        external
        onlyRole(MINTER_ROLE)
    {
        require(to != address(0), "Invalid address");
        require(_tokenIdCounter.current() + quantity <= MAX_SUPPLY, "Exceeds max supply");

        for (uint256 i = 0; i < quantity; i++) {
            _tokenIdCounter.increment();
            uint256 tokenId = _tokenIdCounter.current();

            rarity[tokenId] = rarityLevel;
            _generateAttributes(tokenId, rarityLevel);

            _safeMint(to, tokenId);
            emit NFTMinted(to, tokenId, rarityLevel);
        }
    }

    function setRoyalty(address recipient, uint256 bps)
        external
        onlyRole(ADMIN_ROLE)
    {
        require(bps <= 1000, "Royalty too high"); // Max 10%
        _royaltyRecipient = recipient;
        _royaltyBps = bps;
        emit RoyaltySet(recipient, bps);
    }

    function setBaseURI(string memory baseTokenURI)
        external
        onlyRole(ADMIN_ROLE)
    {
        _baseTokenURI = baseTokenURI;
        emit BaseURIUpdated(baseTokenURI);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        require(_exists(tokenId), "Token does not exist");

        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0
            ? string(abi.encodePacked(baseURI, Strings.toString(tokenId)))
            : "";
    }

    function contractURI() external view returns (string memory) {
        return _contractURI;
    }

    function setContractURI(string memory contractURI_)
        external
        onlyRole(ADMIN_ROLE)
    {
        _contractURI = contractURI_;
    }

    // EIP-2981 Royalty implementation
    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address, uint256)
    {
        require(_exists(tokenId), "Token does not exist");
        uint256 royaltyAmount = (salePrice * _royaltyBps) / 10000;
        return (_royaltyRecipient, royaltyAmount);
    }

    function getAttributes(uint256 tokenId)
        external
        view
        returns (string[] memory traitNames, string[] memory traitValues)
    {
        require(_exists(tokenId), "Token does not exist");

        // Pre-defined trait types
        string[5] memory traitTypes = ["Background", "Body", "Head", "Eyes", "Accessory"];
        string[] memory names = new string[](5);
        string[] memory values = new string[](5);

        for (uint256 i = 0; i < 5; i++) {
            names[i] = traitTypes[i];
            values[i] = attributes[tokenId][traitTypes[i]];
        }

        return (names, values);
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function _generateRarity(uint256 tokenId) private view returns (uint256) {
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            tokenId,
            msg.sender
        )));

        if (random % 100 < 1) return 4; // Legendary (1%)
        if (random % 100 < 5) return 3; // Epic (4%)
        if (random % 100 < 20) return 2; // Rare (15%)
        if (random % 100 < 50) return 1; // Uncommon (30%)
        return 0; // Common (50%)
    }

    function _generateAttributes(uint256 tokenId, uint256 rarityLevel) private {
        // Generate attributes based on rarity
        attributes[tokenId]["Background"] = _getBackground(rarityLevel);
        attributes[tokenId]["Body"] = _getBody(rarityLevel);
        attributes[tokenId]["Head"] = _getHead(rarityLevel);
        attributes[tokenId]["Eyes"] = _getEyes(rarityLevel);
        attributes[tokenId]["Accessory"] = _getAccessory(rarityLevel);
    }

    function _getBackground(uint256 rarity) private pure returns (string memory) {
        string[5] memory backgrounds = ["Blue", "Red", "Green", "Purple", "Gold"];
        return backgrounds[rarity % backgrounds.length];
    }

    function _getBody(uint256 rarity) private pure returns (string memory) {
        string[5] memory bodies = ["Normal", "Muscular", "Slim", "Robot", "Alien"];
        return bodies[rarity % bodies.length];
    }

    function _getHead(uint256 rarity) private pure returns (string memory) {
        string[5] memory heads = ["Normal", "Crown", "Hat", "Helmet", "Halo"];
        return heads[rarity % heads.length];
    }

    function _getEyes(uint256 rarity) private pure returns (string memory) {
        string[5] memory eyes = ["Normal", "Laser", "Glasses", "Patch", "Glowing"];
        return eyes[rarity % eyes.length];
    }

    function _getAccessory(uint256 rarity) private pure returns (string memory) {
        string[5] memory accessories = ["None", "Sword", "Shield", "Wand", "Cape"];
        return accessories[rarity % accessories.length];
    }

    function pause() external onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function withdraw() external onlyRole(ADMIN_ROLE) nonReentrant {
        (bool success, ) = payable(msg.sender).call{value: address(this).balance}("");
        require(success, "Withdrawal failed");
    }
}
```

</example_good>

<example_bad>

```solidity
// BAD: Insecure NFT implementation
contract InsecureNFT {
    // BAD: No proper standards implementation
    mapping(uint256 => address) public ownerOf;
    mapping(address => uint256) public balance;
    uint256 public totalSupply;

    // BAD: No access control
    function mint(address to) public {
        // BAD: No supply limit
        // BAD: No payment validation
        // BAD: No per-address limits
        totalSupply++;
        ownerOf[totalSupply] = to;
        balance[to]++;
    }

    // BAD: No royalty implementation
    // BAD: No metadata standards
    // BAD: No event logging
    // BAD: No security measures
    // BAD: No gas optimization
    // BAD: No rarity system
    // BAD: No attribute validation
}
```

</example_bad>
