import { useState } from 'react';
import { Button, TextInput, View } from 'react-native';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const onLogin = async () => {
    const res = await api.post('/auth/login', { email, password });
    await login(res.data.access_token);
  };

  return (
    <View style={{ padding: 16, gap: 8 }}>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} />
      <TextInput secureTextEntry placeholder="Password" value={password} onChangeText={setPassword} />
      <Button title="Login" onPress={onLogin} />
    </View>
  );
}
