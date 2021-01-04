/*
 * Copyright 2014 International Business Machines Corp.
 * 
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership. Licensed under the Apache License, 
 * Version 2.0 (the "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.ibm.websphere.samples.batch.beans;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;
import javax.persistence.Table;
import javax.persistence.Transient;

@Entity
@Table(name="ACCOUNT", schema="BONUSPAYOUT")
@IdClass(AccountId.class)
public class AccountDataObject {

    // Only currently used for schema gen / table create
    @Id
    @Column(name="INSTANCEID")
    private int instanceId;

    @Id
    @Column(name="ACCTNUM")
    private int accountNumber;

    @Column(name="BALANCE")
    private int balance;

    @Column(name = "ACCTCODE", length = 30)
    private String accountCode;

    @Transient
    private AccountDataObject compareToDataObject;

    public AccountDataObject() {
    }

    /**
     * @param accountNumber
     * @param balance
     * @param accountCode
     */
    public AccountDataObject(int accountNumber, int balance, String accountCode) {
        super();
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.accountCode = accountCode;
    }

    /**
     * @return the accountNumber
     */
    public int getAccountNumber() {
        return accountNumber;
    }

    /**
     * @param accountNumber the accountNumber to set
     */
    public void setAccountNumber(int accountNumber) {
        this.accountNumber = accountNumber;
    }

    /**
     * @return the balance
     */
    public int getBalance() {
        return balance;
    }

    /**
     * @param balance the balance to set
     */
    public void setBalance(int balance) {
        this.balance = balance;
    }

    /**
     * @return the accountCode
     */
    public String getAccountCode() {
        return accountCode;
    }

    /**
     * @param accountCode the accountCode to set
     */
    public void setAccountCode(String accountCode) {
        this.accountCode = accountCode;
    }

    /**
     * @return the compareToDataObject
     */
    public AccountDataObject getCompareToDataObject() {
        return compareToDataObject;
    }

    /**
     * @param compareToDataObject
     */
    public void setCompareToDataObject(AccountDataObject compareToDataObject) {
        this.compareToDataObject = compareToDataObject;
    }

}
