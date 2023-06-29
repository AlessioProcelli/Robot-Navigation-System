/**
 * NumpyLoader.js
 * A simple utility to load NumPy .npy files in JavaScript.
 */

class NumpyLoader {
  constructor() {
    this.urlRegex = /^(https?:\/\/[^\s/$.?#].[^\s]*)$/;
  }

  load(file) {
      console.log("load")
    return new Promise((resolve, reject) => {
      if (this.urlRegex.test(file)) {
        this.loadFromUrl(file, resolve, reject);
      } else {
        this.loadFromFile(file, resolve, reject);
      }
    });
  }

  loadFromUrl(url, resolve, reject) {
    const xhr = new XMLHttpRequest();
    console.log("loadFromUrl")
    xhr.open('POST', url, true);
    xhr.responseType = 'arraybuffer';

    xhr.onload = () => {
      if (xhr.status === 200) {
        const buffer = xhr.response;
        resolve(this.parseBuffer(buffer));
      } else {
        reject(new Error(`Failed to load .npy file: ${url}`));
      }
    };

    xhr.onerror = () => {
      reject(new Error(`Failed to load .npy file: ${url}`));
    };

    xhr.send(null);
  }

  loadFromFile(file, resolve, reject) {
      console.log("loadFromFile")
    const reader = new FileReader();
    reader.onload = () => {
      const buffer = reader.result;
      resolve(this.parseBuffer(buffer));
    };

    reader.onerror = () => {
      reject(new Error(`Failed to load .npy file: ${file.name}`));
    };

    reader.readAsArrayBuffer(file);
  }

  parseBuffer(buffer) {
    const headerLength = 10;
    const version = new Uint8Array(buffer.slice(6, 8));
    const header = new TextDecoder().decode(new Uint8Array(buffer.slice(8, 8 + headerLength)));
    const type = header.includes("'descr': '<f") ? Float32Array : Float64Array;

    const dataOffset = 8 + headerLength;
    const data = new type(buffer.slice(dataOffset));
    return data;
  }
}
