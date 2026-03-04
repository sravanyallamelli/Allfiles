import { useEffect, useState } from 'react';
import { FlatList, Text, View } from 'react-native';
import { api } from '../api/client';

export default function HistoryScreen() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    api.get('/attendance/history').then((res) => setRows(res.data));
  }, []);

  return (
    <FlatList
      data={rows}
      keyExtractor={(item) => String(item.id)}
      renderItem={({ item }) => (
        <View style={{ padding: 12 }}>
          <Text>{item.date} - {item.status}</Text>
        </View>
      )}
    />
  );
}
