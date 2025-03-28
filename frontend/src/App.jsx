import { useState } from 'react';
import './App.css';

export default function App() {
    const [attacks, setAttacks] = useState([]);

    const addAttack = () => {
        setAttacks([
            ...attacks,
            {
                id: Date.now(),
                rollType: '',
                value: '',
                hasExtra: false,
                damageParams: []
            }
        ]);
    };

    const addDamageParam = (attackId) => {
        setAttacks(attacks.map(attack =>
            attack.id === attackId
                ? {
                        ...attack,
                        damageParams: [...attack.damageParams, { damage: '', type: '' }]
                    }
                : attack
        ));
    };

    const handleAttackChange = (attackId, key, value) => {
        setAttacks(attacks.map(attack =>
            attack.id === attackId
                ? { ...attack, [key]: value }
                : attack
        ));
    };

    const handleParamChange = (attackId, paramIndex, key, value) => {
        setAttacks(attacks.map(attack => {
            if (attack.id !== attackId) return attack;
            const updatedParams = [...attack.damageParams];
            updatedParams[paramIndex][key] = value;
            return { ...attack, damageParams: updatedParams };
        }));
    };

    const handleSend = () => {
        console.log('Отправляем данные:', attacks);
        // Можно отправить через fetch() или axios
    };

    const removeDamageParam = (attackId, paramIndex) => {
        setAttacks(attacks.map(attack => {
            if (attack.id !== attackId) return attack;
            const updated = [...attack.damageParams];
            updated.splice(paramIndex, 1);
            return { ...attack, damageParams: updated };
        }));
    };

    return (
        <div className="container">
            <h1 className="title">Кидай кубы</h1>

            <div className="attack-list">
                {attacks.map((attack, attackIndex) => (
                    <div key={attack.id} className="attack-block">
                        <h2>Атака {attackIndex + 1}</h2>

                        <div className="attack-meta">
                            <div className="field-row">
                                <select
                                    value={attack.rollType}
                                    onChange={(e) =>
                                        handleAttackChange(attack.id, 'rollType', e.target.value)
                                    }
                                >
                                    <option value="">Тип атаки</option>
                                    <option value="attack">Бросок атаки</option>
                                    <option value="save">Спасбросок</option>
                                </select>

                                <input
                                    type="number"
                                    placeholder={
                                        attack.rollType === 'save' ? 'Сложность' : 'Модификатор'
                                    }
                                    value={attack.value}
                                    onChange={(e) =>
                                        handleAttackChange(attack.id, 'value', e.target.value)
                                    }
                                />
                            </div>

                            <label className="checkbox">
                                <input
                                    type="checkbox"
                                    checked={attack.hasExtra}
                                    onChange={(e) =>
                                        handleAttackChange(attack.id, 'hasExtra', e.target.checked)
                                    }
                                />
                                {attack.rollType === 'attack'
                                    ? 'Преимущество на атаку'
                                    : 'Половина урона при провале'}
                            </label>
                        </div>

                        <button
                            onClick={() => addDamageParam(attack.id)}
                            className="add-field-btn"
                        >
                            Добавить параметр урона
                        </button>

                        {attack.damageParams.map((param, index) => (
                            <div key={index} className="field-row damage-row">
                                <input
                                    type="text"
                                    placeholder="Урон"
                                    value={param.damage}
                                    onChange={(e) =>
                                        handleParamChange(attack.id, index, 'damage', e.target.value)
                                    }
                                />
                                <input
                                    type="text"
                                    placeholder="Тип урона"
                                    value={param.type}
                                    onChange={(e) =>
                                        handleParamChange(attack.id, index, 'type', e.target.value)
                                    }
                                />
                                <button
                                    className="delete-btn"
                                    onClick={() => removeDamageParam(attack.id, index)}
                                    title="Удалить"
                                >
                                    ❌
                                </button>
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            <div className="add-wrapper">
                <button onClick={addAttack} className="add-btn">
                    Добавить атаку
                </button>
            </div>

            <div className="send-wrapper">
                <button onClick={handleSend} className="send-btn">
                    Отправить данные
                </button>
            </div>
        </div>
    );
}
