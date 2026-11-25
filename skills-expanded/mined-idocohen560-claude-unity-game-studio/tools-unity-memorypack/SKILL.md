---
name: tools-unity-memorypack
description: MemoryPack high-performance binary serialization for Unity including custom formatters, versioning, and performance patterns.
---

# MemoryPack

## Overview

MemoryPack is a high-performance zero-allocation serializer for C#. This skill covers patterns for Unity serialization, custom formatters, and performance optimization.

## When to Use

- Game save data
- Network message serialization
- Asset data serialization
- Cache/persistence systems
- High-frequency serialization needs

## Basic Usage

### Serializable Class

```csharp
using MemoryPack;

[MemoryPackable]
public partial class PlayerSaveData
{
    public string PlayerId;
    public string PlayerName;
    public int Level;
    public float Experience;
    public Vector3 Position;
    public List<ItemData> Inventory;
    public Dictionary<string, int> Statistics;
    
    [MemoryPackConstructor]
    public PlayerSaveData() { }
}

[MemoryPackable]
public partial class ItemData
{
    public string ItemId;
    public int Quantity;
    public int Durability;
}
```

### Serialization/Deserialization

```csharp
public class SaveSystem
{
    public byte[] Serialize<T>(T data)
    {
        return MemoryPackSerializer.Serialize(data);
    }
    
    public T Deserialize<T>(byte[] bytes)
    {
        return MemoryPackSerializer.Deserialize<T>(bytes);
    }
    
    public async UniTask SaveToFileAsync(string path, PlayerSaveData data)
    {
        byte[] bytes = MemoryPackSerializer.Serialize(data);
        await File.WriteAllBytesAsync(path, bytes);
    }
    
    public async UniTask<PlayerSaveData> LoadFromFileAsync(string path)
    {
        if (!File.Exists(path))
            return null;
        
        byte[] bytes = await File.ReadAllBytesAsync(path);
        return MemoryPackSerializer.Deserialize<PlayerSaveData>(bytes);
    }
}
```

## Unity Type Formatters

### Vector3 Formatter

```csharp
using MemoryPack;
using UnityEngine;

public class Vector3Formatter : MemoryPackFormatter<Vector3>
{
    public override void Serialize<TBufferWriter>(
        ref MemoryPackWriter<TBufferWriter> writer, 
        scoped ref Vector3 value)
    {
        writer.WriteUnmanaged(value.x);
        writer.WriteUnmanaged(value.y);
        writer.WriteUnmanaged(value.z);
    }

    public override void Deserialize(
        ref MemoryPackReader reader, 
        scoped ref Vector3 value)
    {
        value.x = reader.ReadUnmanaged<float>();
        value.y = reader.ReadUnmanaged<float>();
        value.z = reader.ReadUnmanaged<float>();
    }
}
```

### Quaternion Formatter

```csharp
public class QuaternionFormatter : MemoryPackFormatter<Quaternion>
{
    public override void Serialize<TBufferWriter>(
        ref MemoryPackWriter<TBufferWriter> writer, 
        scoped ref Quaternion value)
    {
        writer.WriteUnmanaged(value.x);
        writer.WriteUnmanaged(value.y);
        writer.WriteUnmanaged(value.z);
        writer.WriteUnmanaged(value.w);
    }

    public override void Deserialize(
        ref MemoryPackReader reader, 
        scoped ref Quaternion value)
    {
        value.x = reader.ReadUnmanaged<float>();
        value.y = reader.ReadUnmanaged<float>();
        value.z = reader.ReadUnmanaged<float>();
        value.w = reader.ReadUnmanaged<float>();
    }
}
```

### Color Formatter

```csharp
public class ColorFormatter : MemoryPackFormatter<Color>
{
    public override void Serialize<TBufferWriter>(
        ref MemoryPackWriter<TBufferWriter> writer, 
        scoped ref Color value)
    {
        writer.WriteUnmanaged(value.r);
        writer.WriteUnmanaged(value.g);
        writer.WriteUnmanaged(value.b);
        writer.WriteUnmanaged(value.a);
    }

    public override void Deserialize(
        ref MemoryPackReader reader, 
        scoped ref Color value)
    {
        value.r = reader.ReadUnmanaged<float>();
        value.g = reader.ReadUnmanaged<float>();
        value.b = reader.ReadUnmanaged<float>();
        value.a = reader.ReadUnmanaged<float>();
    }
}
```

### Formatter Registration

```csharp
public static class MemoryPackFormatterInitializer
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void Initialize()
    {
        MemoryPackFormatterProvider.Register(new Vector3Formatter());
        MemoryPackFormatterProvider.Register(new QuaternionFormatter());
        MemoryPackFormatterProvider.Register(new ColorFormatter());
        MemoryPackFormatterProvider.Register(new AnimationCurveFormatter());
    }
}
```

## AnimationCurve Formatter

```csharp
public class AnimationCurveFormatter : MemoryPackFormatter<AnimationCurve>
{
    public override void Serialize<TBufferWriter>(
        ref MemoryPackWriter<TBufferWriter> writer, 
        scoped ref AnimationCurve value)
    {
        if (value == null)
        {
            writer.WriteUnmanaged(-1);
            return;
        }
        
        var keys = value.keys;
        writer.WriteUnmanaged(keys.Length);
        
        foreach (var key in keys)
        {
            writer.WriteUnmanaged(key.time);
            writer.WriteUnmanaged(key.value);
            writer.WriteUnmanaged(key.inTangent);
            writer.WriteUnmanaged(key.outTangent);
            writer.WriteUnmanaged(key.inWeight);
            writer.WriteUnmanaged(key.outWeight);
            writer.WriteUnmanaged((int)key.weightedMode);
        }
        
        writer.WriteUnmanaged((int)value.preWrapMode);
        writer.WriteUnmanaged((int)value.postWrapMode);
    }

    public override void Deserialize(
        ref MemoryPackReader reader, 
        scoped ref AnimationCurve value)
    {
        int keyCount = reader.ReadUnmanaged<int>();
        
        if (keyCount < 0)
        {
            value = null;
            return;
        }
        
        var keys = new Keyframe[keyCount];
        
        for (int i = 0; i < keyCount; i++)
        {
            keys[i] = new Keyframe
            {
                time = reader.ReadUnmanaged<float>(),
                value = reader.ReadUnmanaged<float>(),
                inTangent = reader.ReadUnmanaged<float>(),
                outTangent = reader.ReadUnmanaged<float>(),
                inWeight = reader.ReadUnmanaged<float>(),
                outWeight = reader.ReadUnmanaged<float>(),
                weightedMode = (WeightedMode)reader.ReadUnmanaged<int>()
            };
        }
        
        value = new AnimationCurve(keys)
        {
            preWrapMode = (WrapMode)reader.ReadUnmanaged<int>(),
            postWrapMode = (WrapMode)reader.ReadUnmanaged<int>()
        };
    }
}
```

## Polymorphic Serialization

### Union Types

```csharp
[MemoryPackable]
[MemoryPackUnion(0, typeof(MeleeAbilityData))]
[MemoryPackUnion(1, typeof(RangedAbilityData))]
[MemoryPackUnion(2, typeof(AreaAbilityData))]
public abstract partial class AbilityData
{
    public string AbilityId;
    public string DisplayName;
    public float Cooldown;
}

[MemoryPackable]
public partial class MeleeAbilityData : AbilityData
{
    public float Range;
    public float DamageMultiplier;
}

[MemoryPackable]
public partial class RangedAbilityData : AbilityData
{
    public float ProjectileSpeed;
    public float MaxRange;
}

[MemoryPackable]
public partial class AreaAbilityData : AbilityData
{
    public float Radius;
    public float Duration;
}
```

### Usage

```csharp
public class AbilitySerializer
{
    public byte[] SerializeAbility(AbilityData ability)
    {
        return MemoryPackSerializer.Serialize(ability);
    }
    
    public AbilityData DeserializeAbility(byte[] bytes)
    {
        // Automatically deserializes to correct type
        return MemoryPackSerializer.Deserialize<AbilityData>(bytes);
    }
}
```

## Versioning

### Version Tolerant Serialization

```csharp
[MemoryPackable(GenerateType.VersionTolerant)]
public partial class GameSettings
{
    [MemoryPackOrder(0)]
    public float MasterVolume;
    
    [MemoryPackOrder(1)]
    public float MusicVolume;
    
    [MemoryPackOrder(2)]
    public float SfxVolume;
    
    // Added in version 2 - old data will have default value
    [MemoryPackOrder(3)]
    public bool VibrationEnabled;
    
    // Added in version 3
    [MemoryPackOrder(4)]
    public int GraphicsQuality;
}
```

### Handling Missing Fields

```csharp
[MemoryPackable(GenerateType.VersionTolerant)]
public partial class PlayerProgress
{
    [MemoryPackOrder(0)]
    public int Level;
    
    [MemoryPackOrder(1)]
    public long Experience;
    
    [MemoryPackOrder(2)]
    public List<string> UnlockedAbilities;
    
    // Set default for missing field
    [MemoryPackOrder(3)]
    public int Prestige = 0;
    
    [MemoryPackOnDeserializing]
    static void OnDeserializing(ref PlayerProgress value)
    {
        // Initialize collections to prevent null
        value.UnlockedAbilities ??= new List<string>();
    }
}
```

## Performance Patterns

### Buffer Reuse

```csharp
public class OptimizedSerializer
{
    private readonly ArrayBufferWriter<byte> _buffer = new(1024);
    
    public ReadOnlySpan<byte> SerializeReusable<T>(T data)
    {
        _buffer.Clear();
        MemoryPackSerializer.Serialize(_buffer, data);
        return _buffer.WrittenSpan;
    }
    
    public void SerializeToStream<T>(Stream stream, T data)
    {
        _buffer.Clear();
        MemoryPackSerializer.Serialize(_buffer, data);
        stream.Write(_buffer.WrittenSpan);
    }
}
```

### Span-Based Deserialization

```csharp
public class SpanDeserializer
{
    public T DeserializeFromSpan<T>(ReadOnlySpan<byte> span)
    {
        return MemoryPackSerializer.Deserialize<T>(span);
    }
    
    public bool TryDeserialize<T>(ReadOnlySpan<byte> span, out T result)
    {
        try
        {
            result = MemoryPackSerializer.Deserialize<T>(span);
            return true;
        }
        catch
        {
            result = default;
            return false;
        }
    }
}
```

## Network Message Serialization

### Network Message Base

```csharp
[MemoryPackable]
[MemoryPackUnion(0, typeof(MoveMessage))]
[MemoryPackUnion(1, typeof(AttackMessage))]
[MemoryPackUnion(2, typeof(ChatMessage))]
public abstract partial class NetworkMessage
{
    public uint MessageId;
    public long Timestamp;
}

[MemoryPackable]
public partial class MoveMessage : NetworkMessage
{
    public Vector3 Position;
    public Quaternion Rotation;
    public Vector3 Velocity;
}

[MemoryPackable]
public partial class AttackMessage : NetworkMessage
{
    public string AttackerId;
    public string TargetId;
    public string AbilityId;
}

[MemoryPackable]
public partial class ChatMessage : NetworkMessage
{
    public string SenderId;
    public string Content;
    public int Channel;
}
```

### Message Handler

```csharp
public class NetworkMessageHandler
{
    private readonly ArrayBufferWriter<byte> _sendBuffer = new(256);
    
    public byte[] PackMessage(NetworkMessage message)
    {
        _sendBuffer.Clear();
        MemoryPackSerializer.Serialize(_sendBuffer, message);
        return _sendBuffer.WrittenSpan.ToArray();
    }
    
    public NetworkMessage UnpackMessage(byte[] data)
    {
        return MemoryPackSerializer.Deserialize<NetworkMessage>(data);
    }
    
    public void HandleMessage(byte[] data)
    {
        var message = UnpackMessage(data);
        
        switch (message)
        {
            case MoveMessage move:
                HandleMove(move);
                break;
            case AttackMessage attack:
                HandleAttack(attack);
                break;
            case ChatMessage chat:
                HandleChat(chat);
                break;
        }
    }
}
```

## Ignore and Custom Serialization

### Ignoring Fields

```csharp
[MemoryPackable]
public partial class EntityState
{
    public string EntityId;
    public Vector3 Position;
    public float Health;
    
    // Don't serialize - computed at runtime
    [MemoryPackIgnore]
    public bool IsDead => Health <= 0;
    
    // Don't serialize - reference to scene object
    [MemoryPackIgnore]
    public GameObject GameObjectRef;
    
    // Don't serialize - cached component
    [MemoryPackIgnore]
    public Transform TransformRef;
}
```

### Custom Serialize Logic

```csharp
[MemoryPackable]
public partial class CustomSerializable : IMemoryPackable<CustomSerializable>
{
    public int Value;
    public string Name;
    
    // Custom validation on deserialize
    static void IMemoryPackable<CustomSerializable>.Deserialize(
        ref MemoryPackReader reader, 
        scoped ref CustomSerializable value)
    {
        value ??= new CustomSerializable();
        
        value.Value = reader.ReadUnmanaged<int>();
        value.Name = reader.ReadString();
        
        // Validate after deserialize
        if (value.Value < 0)
            value.Value = 0;
            
        if (string.IsNullOrEmpty(value.Name))
            value.Name = "Default";
    }
}
```

## Best Practices

1. **Use partial classes** with [MemoryPackable]
2. **Register Unity formatters** on initialization
3. **Use VersionTolerant** for save data
4. **Reuse buffers** for high-frequency serialization
5. **Use unions** for polymorphic types
6. **Ignore runtime references** - GameObjects, Components
7. **Initialize collections** in OnDeserializing
8. **Test serialization roundtrip** in unit tests
9. **Profile serialization** performance
10. **Handle version migration** gracefully

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Type not serializable | Add [MemoryPackable] and partial |
| Unity type fails | Register custom formatter |
| Null collection after load | Initialize in OnDeserializing |
| Wrong type deserialized | Check union attribute order |
| Old save won't load | Use VersionTolerant generation |
| Large serialized size | Check for unneeded fields |
