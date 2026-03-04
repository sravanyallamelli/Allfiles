import { useState } from 'react';
import { Button, TextInput, View } from 'react-native';
import { api } from '../api/client';

export default function LeaveScreen() {
  const [fromDate, setFromDate] = useState('2026-01-01');
  const [toDate, setToDate] = useState('2026-01-01');
  const [reason, setReason] = useState('Personal');

  const apply = () => api.post('/leave-requests', { from_date: fromDate, to_date: toDate, reason });

  return (
    <View style={{ padding: 16, gap: 8 }}>
      <TextInput placeholder="From (YYYY-MM-DD)" value={fromDate} onChangeText={setFromDate} />
      <TextInput placeholder="To (YYYY-MM-DD)" value={toDate} onChangeText={setToDate} />
      <TextInput placeholder="Reason" value={reason} onChangeText={setReason} />
      <Button title="Apply" onPress={apply} />
    </View>
  );
}
