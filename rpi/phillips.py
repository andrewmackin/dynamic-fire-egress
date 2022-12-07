QUERY = (
"CREATE "
  "(e1:Exit:Sign {id:1, dir: 'up'}),"
  "(e2:Exit {id:2, dir:'none'}),"
  "(e3:Exit:Sign {id:3, dir: 'right'}),"
  "(e4:Exit:Sign {id:12, dir: 'up'}),"
  "(s1:Sign {id:4, dir: 'right'}),"
  "(s2:Sign {id:13, dir: 'up'}),"
  "(r1:Alarm {id: 5}),"
  "(r2:Alarm {id:6}),"
  "(r3:Alarm {id:7}),"
  "(d1:Delta {id:8, dist: 3, dir:'left'}),"
  "(d2:Delta {id:9, dist: 1, dir:'right'}),"
  "(d3:Delta {id:10, dist:4, dir:'up'}),"
  "(d4:Delta {id:11, dist:5, dir:'down'}),"
  "(d5:Delta {id:14, dist: 1, dir:'left'}),"
  "(d6:Delta {id:15, dist: 3, dir:'down'}),"
  "(d7:Delta {id:16, dist: 6, dir:'up'}),"
  "(d8:Delta {id:17, dist: 4, dir:'right'}),"
  "(r1)-[:CONNECTED_TO {cost: 0}]->(d3),"
  "(r2)-[:CONNECTED_TO {cost: 0}]->(d4),"
  "(r3)-[:CONNECTED_TO {cost: 0}]->(d1),"
  "(r1)-[:CONNECTED_TO {cost: 0}]->(d6),"
  "(r2)-[:CONNECTED_TO {cost: 0}]->(d7),"
  "(r3)-[:CONNECTED_TO {cost: 0}]->(d8),"
  "(s1)-[:CONNECTED_TO {cost: 0}]->(d1),"
  "(d1)-[:CONNECTED_TO {cost: 3}]->(e3),"
  "(s1)-[:CONNECTED_TO {cost: 0}]->(d4),"
  "(d4)-[:CONNECTED_TO {cost: 5}]->(e4),"
  "(s1)-[:CONNECTED_TO {cost: 0}]->(d2),"
  "(d2)-[:CONNECTED_TO {cost: 1}]->(e2),"
  "(s1)-[:CONNECTED_TO {cost: 0}]->(d3),"
  "(d3)-[:CONNECTED_TO {cost: 4}]->(e1),"
  "(s2)-[:CONNECTED_TO {cost: 0}]->(d8),"
  "(d8)-[:CONNECTED_TO {cost: 4}]->(e3),"
  "(s2)-[:CONNECTED_TO {cost: 0}]->(d7),"
  "(d7)-[:CONNECTED_TO {cost: 6}]->(e4),"
  "(s2)-[:CONNECTED_TO {cost: 0}]->(d5),"
  "(d5)-[:CONNECTED_TO {cost: 1}]->(e2),"
  "(s2)-[:CONNECTED_TO {cost: 0}]->(d6),"
  "(d6)-[:CONNECTED_TO {cost: 3}]->(e1);"
)