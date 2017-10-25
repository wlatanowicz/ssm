import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  url = 'ws://localhost:8000';
  deviceId = '12345-67890';
  measureInterval = 100;
  packetSize = 10;

  connection: any = null;

  measures: any[] = [];


  ngOnInit(): void {
    setTimeout(this.performMeasure.bind(this), 1000);
  }

  connect() {
    this.connection = new WebSocket(this.url);
  }

  disconnect() {
    this.connection.close();
  }

  performMeasure() {
    if (this.isConnected()) {
      this.measure();
      this.send();
      setTimeout(this.performMeasure.bind(this), this.measureInterval);
    } else {
      setTimeout(this.performMeasure.bind(this), 1000);
    }
  }

  send() {
    if (this.measures.length > 0 && this.measures.length >= this.packetSize) {
      let data = null;
      if (this.packetSize == 0) {
        data = this.measures.shift();
      } else {
        data = this.measures.splice(0, this.packetSize);
      }
      this.connection.send(JSON.stringify(data));
      console.log('data to send', data);
    }
  }

  measure() {
    this.measures.push({
      id: this.deviceId,
      s: Math.random() * 1000,
    });
  }

  isConnected() {
    return this.connection && this.connection.readyState === 1;
  }
}
