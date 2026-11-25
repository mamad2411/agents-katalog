---
name: sky-web3
description: >-
  Web3 ve blok zinciri uygulama geliştirme: EVM temelleri (hesap, işlem, gas, ağ), cüzdan
  bağlama (wagmi + viem, RainbowKit/ConnectKit), zincirden okuma/yazma ve işlem durumu, Solidity
  akıllı sözleşme temelleri ve yaygın standartlar (ERC-20/721/1155), Foundry/Hardhat ile
  geliştirme ve test, güvenlik (reentrancy, erişim kontrolü, denetim), olayları dinleme ve
  indeksleme (The Graph), imza ile kimlik (SIWE), cüzdansız (hesap soyutlama) ve ölçek (L2).
  Blok zinciri, kripto cüzdan, NFT, akıllı sözleşme veya dapp projesinde kullan.
disable-model-invocation: true
---

# Sky · Web3

## Temeller

EVM ağları (Ethereum + L2'ler: Base, Arbitrum, Optimism, Polygon). Hesap = adres; işlem imzalı + **gas** ücreti; ağlar `chainId` ile; testnet'te geliştir (Sepolia). Zincir **herkese açık ve değiştirilemez** — hassas veri zincire yazılmaz, özel anahtar asla sunucuda/kodda değildir.

## Ön yüz: cüzdan bağlama

```ts
import { createConfig, http } from "wagmi";
import { base, mainnet } from "wagmi/chains";
const config = createConfig({ chains: [mainnet, base], transports: { [mainnet.id]: http(), [base.id]: http() } });
// RainbowKit/ConnectKit: hazır "Cüzdan bağla" UI, ağ değiştirme, bakiye
const { data } = useReadContract({ address, abi, functionName: "balanceOf", args: [user] });
const { writeContract } = useWriteContract();   // kullanıcı cüzdanda onaylar; işlem hash'i → bekle
```
- **viem** (tip güvenli) + **wagmi** (React hook'ları) modern standart; RainbowKit/ConnectKit bağlan deneyimini halleder.
- Yazma işlemleri kullanıcının cüzdanında imzalanır — uygulama özel anahtar tutmaz; işlem onayı, gas tahmini ve "beklemede/onaylandı/başarısız" durumunu net göster.
- Okuma ucuz (RPC), yazma gas maliyetli; kullanıcıya maliyeti ve ne imzaladığını açıkça göster (kör imza = phishing riski).

## Akıllı sözleşme (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract Vault is Ownable, ReentrancyGuard {
    mapping(address => uint256) public balances;
    event Withdrawn(address indexed user, uint256 amount);
    constructor() Ownable(msg.sender) {}
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "yetersiz bakiye");
        balances[msg.sender] -= amount;                 // önce durum güncelle (checks-effects-interactions)
        (bool ok, ) = msg.sender.call{value: amount}(""); require(ok, "transfer başarısız");
        emit Withdrawn(msg.sender, amount);
    }
}
```
- **OpenZeppelin** denetlenmiş bileşenlerini kullan (standartlar, erişim kontrolü, güvenlik); sıfırdan yazma.
- Güvenlik: reentrancy (checks-effects-interactions + `nonReentrant`), erişim kontrolü (`onlyOwner`/roller), tamsayı (0.8+ otomatik taşma kontrolü), `tx.origin` kullanma, harici çağrı dönüşlerini kontrol et, fiyat oracle manipülasyonu.
- Sözleşmeler **değiştirilemez ve para tutar** → hata pahalı: kapsamlı test, testnet, bağımsız **denetim** (audit) ve/veya ödül programı yayından önce.

## Araçlar

- **Foundry** (Solidity ile test — hızlı, fuzz testi, `forge test`) veya Hardhat (JS/TS ekosistemi). `forge coverage`, Slither (statik analiz), mainnet fork testi.
- Dağıtım script'leri sürüm kontrollü; sözleşme adresleri ve ABI'ler ön yüze paylaşılan pakette.

## Zincir verisi

Olayları dinle (`watchContractEvent`) veya **indeksle**: The Graph / Ponder ile olayları sorgulanabilir DB'ye yaz (kullanıcı geçmişi, lider tablosu). Zincirden her şeyi okumak yavaş ve pahalı; indeks + önbellek (bkz. `sky-caching`).

## Kimlik ve UX

- **SIWE** (Sign-In with Ethereum): cüzdan imzasıyla giriş (nonce ile, sunucuda doğrula) — gaz maliyeti yok.
- Hesap soyutlama (ERC-4337) / gömülü cüzdanlar (Privy, Dynamic) ile "cüzdansız" kullanıcıya e-posta/sosyal girişle Web3 deneyimi.
- L2 kullan (düşük gaz); işlem beklerken iyimser UI ama kesinleşmeyi (confirmation) bekle; başarısız işlemi anlaşılır açıkla.

## Dolandırıcılık ve sorumluluk

Kullanıcıları koru: ne imzaladıklarını açık göster, sınırsız onay (`approve` max) yerine gereken miktar, bilinen phishing kalıplarına karşı uyarı, resmi sözleşme adreslerini doğrula. Finansal tavsiye verme; risklere dikkat çek.
