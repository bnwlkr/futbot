//
//  ViewController.swift
//  futbot-ios
//
//  Created by Ben Walker on 2018-09-04.
//  Copyright © 2018 Ben Walker. All rights reserved.
//

import UIKit
import Starscream

class ViewController: UIViewController, WebSocketDelegate {
    
    
    var socket: WebSocket!
    @IBOutlet weak var log: UITextView!
    @IBOutlet weak var activity: UIActivityIndicatorView!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        var request = URLRequest(url: URL(string: "ws://wallnet.ca:8000")!)
        request.timeoutInterval = 5
        socket = WebSocket(request: request)
        socket.delegate = self
        log.isEditable = false
        activity.isHidden = true
    }
    
    
    func websocketDidConnect(socket: WebSocketClient) {
        activity.isHidden = false
        activity.startAnimating()
    }
    
    func websocketDidDisconnect(socket: WebSocketClient, error: Error?) {
        activity.isHidden = true
        activity.stopAnimating()
    }
    
    func websocketDidReceiveMessage(socket: WebSocketClient, text: String) {
        log.text = log.text + text + "\n"
    }
    
    func websocketDidReceiveData(socket: WebSocketClient, data: Data) {}
    
    
    @IBAction func run(_ sender: UIButton) {
        socket.connect()
    }
    
}
